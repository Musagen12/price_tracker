import time
import re
from fake_useragent import UserAgent
from seleniumwire import webdriver  
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from requests_html import HTML
from api.amazon import schemas


# Generate a random user agent
useragent = UserAgent()

# Interceptor function to set request headers
def interceptor(request):
    request.headers["Accept-Language"] = "en-US,en;q=0.9"
    request.headers["Referer"] = "https://www.google.com/"
    request.headers["User-Agent"] = useragent.random  

def get_product_details(search_query: str, max_pages: int = 10):
    base_url = "https://www.amazon.com/s?k=" + search_query.replace(' ', '+') + "&page="

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.page_load_strategy = "normal"
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    driver.request_interceptor = interceptor

    products = []
    
    try:
        for current_page in range(1, max_pages + 1):
            page_url = base_url + str(current_page)
            print(f"Scraping page {current_page}: {page_url}")
            driver.get(page_url)

            # Wait for the search results to load
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.s-main-slot"))
            )
            time.sleep(3)  # Let the page fully load

            # Get the page source and parse it with requests_html.HTML
            html_str = driver.page_source
            html_object = HTML(html=html_str)

            # Find all products
            product_cards = html_object.find('div[data-component-type="s-search-result"]')

            # Loop through each product and extract details
            for product in product_cards:
                try:
                    asin = product.attrs.get('data-asin')
                    name = product.find('span.a-text-normal', first=True).text
                    price_whole = product.find('span.a-price-whole', first=True)
                    price_fraction = product.find('span.a-price-fraction', first=True)
                    price = None

                    if price_whole and price_fraction:
                        price_str = f"{price_whole.text}{price_fraction.text}"
                        # Convert price to float, removing any non-numeric characters
                        price = float(re.sub(r'[^\d.]', '', price_str))

                    # Initialize in_stock with a default value
                    in_stock = "Not in stock"
                    stock_status = product.find('span.a-color-price', first=True)
                    if stock_status:
                        in_stock = stock_status.text.strip()

                    # Only add the product if the price is available and it's in stock
                    if price is not None and in_stock != "Not in stock":
                        img_element = product.find('img', first=True)
                        image_url = img_element.attrs['src'] if img_element else None
                        url = f"https://www.amazon.com/dp/{asin}"

                        products.append({
                            'asin': asin,
                            'name': name,
                            'price': price,  # Now a float
                            'rating': product.find('span.a-icon-alt', first=True).text if product.find('span.a-icon-alt', first=True) else "No rating",
                            'in_stock': in_stock,
                            'image_url': image_url, 
                            'url': url
                        })
                except Exception as e:
                    print(f"Error extracting product details on page {current_page}: {e}")

    except TimeoutException as e:
        print(f"TimeoutException: {e}")

    finally:
        driver.quit()

    return products

def amazon_search(search_query: str):
    products = get_product_details(search_query, max_pages=10)
    
    product_data = {"products": products}
    
    product_list = schemas.ProductList(**product_data)
    return product_list


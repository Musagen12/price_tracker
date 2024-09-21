import time
from fake_useragent import UserAgent
from seleniumwire import webdriver  
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from requests_html import HTML

useragent = UserAgent()

def interceptor(request):
    request.headers["Accept-Language"] = "en-US,en;q=0.9"
    request.headers["Referer"] = "https://www.google.com/"
    request.headers["User-Agent"] = useragent.random  

def get_product_details(search_query: str, max_pages: int = 6):
    base_url = "https://www.jumia.co.ke/catalog/?q=" + search_query + "&page="
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.page_load_strategy = "normal"

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
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.-paxs"))
            )
            time.sleep(3)  # Let the page fully load

            # Get the page source and parse it with requests_html.HTML
            html_str = driver.page_source
            html_object = HTML(html=html_str)

            # Find all products
            product_cards = html_object.find('article.prd')

            # Stop scraping if no products found
            if not product_cards:
                print(f"No products found on page {current_page}. Stopping.")
                break

            # Loop through each product and extract details
            for product in product_cards:
                try:
                    name = product.find('h3.name', first=True).text
                    price = product.find('div.prc', first=True).text
                    rating_element = product.find('div.stars', first=True)
                    rating = rating_element.text if rating_element else "No rating"
                    in_stock = product.find('p.-fs12', first=True).text if product.find('p.-fs12', first=True) else "In stock"
                    image_url = product.find('img.img', first=True).attrs.get('data-src')
                    product_url = product.find('a.core', first=True).attrs.get('href')
                    full_product_url = "https://www.jumia.co.ke" + product_url
                    brand = product.find('a.core', first=True).attrs.get('data-gtm-brand', 'Unknown')

                    products.append({
                        'name': name,
                        'price': price,
                        'rating': rating,
                        'in_stock': in_stock,
                        'image_url': image_url, 
                        'brand': brand,
                        'url': full_product_url
                    })
                except Exception as e:
                    print(f"Error extracting product details on page {current_page} for product: {product.html}. Error: {e}")

    except TimeoutException as e:
        print(f"TimeoutException: {e}")

    finally:
        driver.quit()

    return products

def jumia_search(search_query: str):
    products = get_product_details(search_query, max_pages=6)

    for product in products:
        print(product)

jumia_search(search_query="lenovo")
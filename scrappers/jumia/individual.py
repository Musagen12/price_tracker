import time
import re
from fake_useragent import UserAgent
from seleniumwire import webdriver  
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from requests_html import HTML

useragent = UserAgent()

def interceptor(request):
    request.headers["Accept-Language"] = "en-US,en;q=0.9"
    request.headers["Referer"] = "https://www.google.com/"
    request.headers["User-Agent"] = useragent.random  

def clean_price(price_str: str):
    """Extract the numeric part from a price string."""
    price_match = re.search(r'\d+', price_str.replace(",", ""))
    return int(price_match.group()) if price_match else None

def get_product_details(url: str):    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")  # Uncomment this for headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.page_load_strategy = "normal"

    driver = webdriver.Chrome(options=chrome_options)
    driver.request_interceptor = interceptor
    
    results = {}
    
    try:
        driver.get(url)
        WebDriverWait(driver, 80).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.row"))
        )

        # Get the page source and parse it with requests_html.HTML
        html_str = driver.page_source
        html_object = HTML(html=html_str)

        try:
            # Extract product details
            name_element = html_object.find('h1.-pbxs', first=True)
            name = name_element.text if name_element else "Name not found"
            
            price_str_element = html_object.find('span.-b', first=True)
            price_str = price_str_element.text if price_str_element else "Price not found"
            price = clean_price(price_str) if price_str != "Price not found" else None

            rating_element = html_object.find('div.stars', first=True)
            rating = rating_element.text if rating_element else "No rating"

            in_stock_element = html_object.find('p.-fs12', first=True)
            in_stock = in_stock_element.text if in_stock_element else "In stock information not available"

            image_url_element = html_object.find('img.-fw', first=True)
            image_url = image_url_element.attrs.get('data-src', 'No image available') if image_url_element else 'No image available'

            try:
                brand_element = driver.find_element(By.CSS_SELECTOR, "div.-pvxs a._more")
                brand = brand_element.text if brand_element else "Brand not found"
            except NoSuchElementException:
                brand = "Brand not found"

            results = {
                'name': name,
                'price': price,
                'rating': rating,
                'in_stock': in_stock,
                'image_url': image_url,
                'brand': brand,
                'url': url
            }
        except Exception as e:
            print(f"Error extracting product details: {e}")
            return {}  # Return an empty dict in case of error
   
    except TimeoutException as e:
        print(f"TimeoutException: {e}")
        return {"error": "Page load timeout"}
    
    finally:
        driver.quit()

    return results

def get_individual_jumia_item(url: str):
    results = get_product_details(url)
    return results

# get = get_individual_jumia_item(url="https://www.jumia.co.ke/hikers-43-inch-frameless-android-smart-fhd-led-tv-black-130121825.html")
# print(get)

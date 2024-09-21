import time
import concurrent
from fake_useragent import UserAgent
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from requests_html import HTML

# Generate a random user agent
useragent = UserAgent()
random_useragent = useragent.random

# Interceptor function to set request headers
def interceptor(request):
    request.headers["Accept-Language"] = "en-US,en;q=0.9"
    request.headers["Referer"] = "https://www.google.com/"
    request.headers["User-Agent"] = random_useragent

def get_product_details(search_query: str):
    url = "https://www.amazon.com"

    # Configure WebDriver options
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.page_load_strategy = "normal"  # Changed to "normal"
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Initialize WebDriver with interceptor
    driver = webdriver.Chrome(options=chrome_options)
    driver.request_interceptor = interceptor

    products = []

    try:
        driver.get(url)

        # Wait for the search bar to be present
        search_bar = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
        )
        search_bar.send_keys(search_query)
        search_bar.send_keys(Keys.RETURN)

        # Wait for the search results to load
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.s-main-slot"))
        )

        # Get the page source
        html_str = driver.page_source

        # Parse the HTML to extract product details
        html_object = HTML(html=html_str)
        for product in html_object.find('div[data-component-type="s-search-result"]'):
            try:
                asin = product.attrs.get('data-asin')
                name = product.find('span.a-text-normal', first=True).text
                price_whole = product.find('span.a-price-whole', first=True)
                price_fraction = product.find('span.a-price-fraction', first=True)
                price = None
                if price_whole and price_fraction:
                    price = f"{price_whole.text}{price_fraction.text}"
                rating = product.find('span.a-icon-alt', first=True)
                rating = rating.text if rating else None
                delivery = product.find('span.s-align-children-center', first=True)
                delivery = delivery.text if delivery else "Not specified"

                products.append({
                    'asin': asin,
                    'name': name,
                    'price': price,
                    'rating': rating,
                    'delivery': delivery
                })
            except Exception as e:
                print(f"Error extracting product details: {e}")

    except TimeoutException as e:
        print(f"TimeoutException: {e}")

    finally:
        driver.quit()

    return products

def amazon_search(search_query: str):
    products = get_product_details(search_query)
    for product in products:
        print(product)

amazon_search(search_query="laptop")


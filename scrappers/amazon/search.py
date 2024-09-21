# import time
# import concurrent
# from fake_useragent import UserAgent
# from seleniumwire import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException, NoSuchElementException
# from requests_html import HTML

# # Generate a random user agent
# useragent = UserAgent()
# random_useragent = useragent.random

# # Interceptor function to set request headers
# def interceptor(request):
#     request.headers["Accept-Language"] = "en-US,en;q=0.9"
#     request.headers["Referer"] = "https://www.google.com/"
#     request.headers["User-Agent"] = random_useragent

# def extract_table_data(html_object):
#     """Extract product data from HTML table elements."""
#     dataset = {}
#     tables = html_object.find('table')

#     for table in tables:
#         for tbody in table.element.getchildren():
#             for tr in tbody.getchildren():
#                 row = [col.text_content().strip() for col in tr.getchildren() if col.text_content()]
#                 if len(row) == 2:
#                     key, value = row
#                     key = key.replace("-", "_")
#                     dataset[key] = value

#     return dataset

# # def extract_table_data(html_object):
# #     """Extract product data from HTML table elements."""
# #     dataset = {}
# #     tables = html_object.find('table')

# #     for table in tables:
# #         for tbody in table.element.getchildren():
# #             for tr in tbody.getchildren():
# #                 row = [col.text_content().strip() for col in tr.getchildren() if col.text_content()]
# #                 if len(row) == 2:
# #                     key, value = row
# #                     key = key.replace("-", "_")
# #                     if "$" in value:
# #                         new_value = extract_price_from_string(value)
# #                         dataset[key] = new_value or value
# #                     else:
# #                         dataset[key] = value

# #     return dataset

# def get_product_details(dataset):
#     manufacturer = dataset.get('Manufacturer', "Manufacturer not available")
#     total_price = dataset.get('Total', "Total price not available")
#     return manufacturer, total_price

# def get_product_details(search_query: str, max_pages: int = 6):
#     products = []
#     base_url = "https://www.amazon.com/s?k=" + search_query.replace(' ', '+') + "&page="

#     # Configure WebDriver options
#     chrome_options = webdriver.ChromeOptions()
#     # chrome_options.add_argument("--headless")
#     chrome_options.add_argument("--disable-gpu")
#     chrome_options.add_argument("--no-sandbox")
#     chrome_options.page_load_strategy = "normal"
#     chrome_options.add_argument("--disable-dev-shm-usage")

#     # Initialize WebDriver with interceptor
#     driver = webdriver.Chrome(options=chrome_options)
#     driver.request_interceptor = interceptor

#     try:
#         for page in range(1, max_pages + 1):
#             driver.get(base_url + str(page))

#             # Wait for the search results to load
#             WebDriverWait(driver, 30).until(
#                 EC.presence_of_element_located((By.CSS_SELECTOR, "div.s-main-slot"))
#             )

#             # Get the page source
#             html_str = driver.page_source

#             # Parse the HTML to extract product details
#             html_object = HTML(html=html_str)
#             for product in html_object.find('div[data-component-type="s-search-result"]'):
#                 try:
#                     asin = product.attrs.get('data-asin')
#                     name = product.find('span.a-text-normal', first=True).text
#                     price_whole = product.find('span.a-price-whole', first=True)
#                     price_fraction = product.find('span.a-price-fraction', first=True)
#                     price = None
#                     if price_whole and price_fraction:
#                         price = f"{price_whole.text}{price_fraction.text}"
#                     rating = product.find('span.a-icon-alt', first=True)
#                     rating = rating.text if rating else None
#                     stock_status = html_object.find("#availability", first=True)
#                     in_stock = stock_status.text.strip() if stock_status else "Not in stock"
#                     img_element = product.find('img', first=True)
#                     image_url = img_element.attrs['src'] if img_element else None
#                     url = f"https://www.amazon.com/dp/{asin}"

#                     dataset = extract_table_data(html_object)
#                     manufacturer, total_price = get_product_details(dataset)

#                     products.append({
#                         'asin': asin,
#                         'name': name,
#                         'price': price,
#                         'total_price': total_price,
#                         'rating': rating,
#                         'delivery': delivery,
#                         'image_url': image_url,
#                         'url': url,
#                         'manufacturer': manufacturer,
#                         'in_stock': in_stock  
#                     })
#                 except Exception as e:
#                     print(f"Error extracting product details: {e}")

#     except TimeoutException as e:
#         print(f"TimeoutException: {e}")

#     finally:
#         driver.quit()

#     return products



# def amazon_search(search_query: str):
#     products = get_product_details(search_query)
#     for product in products:
#         print(product)

# amazon_search(search_query="laptop")

import time
from fake_useragent import UserAgent
from seleniumwire import webdriver  
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from requests_html import HTML

# Generate a random user agent
useragent = UserAgent()

# Interceptor function to set request headers
def interceptor(request):
    request.headers["Accept-Language"] = "en-US,en;q=0.9"
    request.headers["Referer"] = "https://www.google.com/"
    request.headers["User-Agent"] = useragent.random  

def get_product_details(search_query: str, max_pages: int = 6):
    base_url = "https://www.amazon.com/s?k=" + search_query.replace(' ', '+') + "&page="

    chrome_options = webdriver.ChromeOptions()
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
                        price = f"{price_whole.text}{price_fraction.text}"
                    rating = product.find('span.a-icon-alt', first=True)
                    rating = rating.text if rating else "No rating"
                    stock_status = product.find('span.a-color-price', first=True)
                    in_stock = stock_status.text.strip() if stock_status else "Not in stock"
                    img_element = product.find('img', first=True)
                    image_url = img_element.attrs['src'] if img_element else None
                    url = f"https://www.amazon.com/dp/{asin}"

                    products.append({
                        'asin': asin,
                        'name': name,
                        'price': price,
                        'rating': rating,
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
    products = get_product_details(search_query, max_pages=6)
    for product in products:
        print(product)

# Example usage
amazon_search(search_query="laptop")

import time
import re
from selenium import webdriver  
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from requests_html import HTML
from api.jumia import schemas

def get_product_details(search_query: str, max_pages: int = 6):
    base_url = "https://www.jumia.co.ke/catalog/?q=" + search_query + "&page="
    site_url = "https://www.jumia.co.ke"
    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.page_load_strategy = "normal"

    driver = webdriver.Chrome(options=chrome_options)
    products = []
    
    try:
        for current_page in range(1, max_pages + 1):
            page_url = base_url + str(current_page)
            print(f"Scraping page {current_page}: {page_url}")
            driver.get(page_url)
            
            try:
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.-paxs"))
                )
            except TimeoutException:
                continue
            
            time.sleep(3)  

            html_str = driver.page_source
            html = HTML(html=html_str)
            
            product_cards = html.find("article.prd")

            if not product_cards:
                break

            for product in product_cards:
                try:
                    name = product.find('h3.name', first=True).text
                    price_str = product.find('div.prc', first=True).text
                    rating_element = product.find('div.stars._s', first=True)
                    rating = rating_element.text.split(' ')[0] if rating_element else "No rating"  # Get the numeric part of the rating

                    in_stock = product.find('p.-fs12', first=True).text if product.find('p.-fs12') else "In stock"
                    image_url = product.find('img.img', first=True).attrs.get('data-src', '')
                    product_url_str = product.find('a.core', first=True).attrs.get('href', '')
                    product_url = site_url + product_url_str


                    products.append({
                        'name': name,
                        'price': price_str,
                        'rating': rating,
                        'in_stock': in_stock,
                        'image_url': image_url, 
                        'url': product_url
                    })
                except Exception as e:
                    print(f"Error extracting product details on page {current_page}: {e}")

            time.sleep(2)  

    finally:
        driver.quit()

    return products

def jumia_search(search_query: str):
    products = get_product_details(search_query, max_pages=6)

    product_data = {"products": products}
    
    product_list = schemas.ProductList(**product_data)
    return product_list
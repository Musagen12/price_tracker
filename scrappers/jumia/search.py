import time
import re
from fake_useragent import UserAgent
from selenium import webdriver  
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

useragent = UserAgent()

def get_product_details(search_query: str, max_pages: int = 6):
    base_url = "https://www.jumia.co.ke/catalog/?q=" + search_query + "&page="
    
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
            
            # Wait for the search results to load
            try:
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.-paxs"))
                )
            except TimeoutException:
                print(f"Timeout waiting for elements on page {current_page}.")
                continue
            
            time.sleep(3)  # Allow the page to load

            # Get the page source and check for loaded content
            html_str = driver.page_source
            print(f"Page {current_page} source length: {len(html_str)}")  # Check if the page source is loaded
            
            # Find all products
            product_cards = driver.find_elements(By.CSS_SELECTOR, "article.prd")
            print(f"Found {len(product_cards)} products on page {current_page}.")  # Debug info

            # Stop scraping if no products found
            if not product_cards:
                print(f"No products found on page {current_page}. Stopping.")
                break

            # Loop through each product and extract details
            for product in product_cards:
                try:
                    name = product.find_element(By.CSS_SELECTOR, 'h3.name').text
                    price_str = product.find_element(By.CSS_SELECTOR, 'div.prc').text
                    price = re.search(r'\d+', price_str.replace(",", "")).group()  # Extract price
                    rating_element = product.find_element(By.CSS_SELECTOR, 'div.stars')
                    rating = rating_element.text if rating_element else "No rating"
                    in_stock = product.find_element(By.CSS_SELECTOR, 'p.-fs12').text if product.find_elements(By.CSS_SELECTOR, 'p.-fs12') else "In stock"
                    image_url = product.find_element(By.CSS_SELECTOR, 'img.img').get_attribute('data-src')
                    product_url = product.find_element(By.CSS_SELECTOR, 'a.core').get_attribute('href')

                    products.append({
                        'name': name,
                        'price': price,
                        'rating': rating,
                        'in_stock': in_stock,
                        'image_url': image_url, 
                        'url': product_url
                    })
                except Exception as e:
                    print(f"Error extracting product details on page {current_page}: {e}")

            time.sleep(2)  # Delay between page requests to avoid rate limiting

    finally:
        driver.quit()

    return products

def jumia_search(search_query: str):
    products = get_product_details(search_query, max_pages=6)

    for product in products:
        print(product)

jumia_search(search_query="lenovo")

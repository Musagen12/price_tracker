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

def get_product_details(url: str):    
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.page_load_strategy = "normal"

    driver = webdriver.Chrome(options=chrome_options)
    driver.request_interceptor = interceptor
    
    results = {}
    
    try:
        driver.get(url)
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.row"))
        )
        time.sleep(3)  # Let the page fully load

        # Get the page source and parse it with requests_html.HTML
        html_str = driver.page_source
        html_object = HTML(html=html_str)

        try:
            # Extract product details
            name = html_object.find('h1.-pbxs', first=True).text
            price = html_object.find('span.-b', first=True).text
            rating_element = html_object.find('div.stars', first=True)
            rating = rating_element.text if rating_element else "No rating"
            in_stock = html_object.find('p.-fs12', first=True).text if html_object.find('p.-fs12', first=True) else "In stock"
            image_url = html_object.find('img.-fw', first=True).attrs.get('data-src')
            brand_element = driver.find_element(By.CSS_SELECTOR, "div.-pvxs a._more")
            brand = brand_element.text

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
   
    except TimeoutException as e:
        print(f"TimeoutException: {e}")

    finally:
        driver.quit()

    return results

def get_individual_jumia_item(url: str):
    results = get_product_details(url)
    print(results)

get_individual_jumia_item(url="https://www.jumia.co.ke/lenovo-refurbished-thinkpad-11e-b-11.6-intel-celeron-4gb-128gb-ssd-black-6m-wry-96969127.html")
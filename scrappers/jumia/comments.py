from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from requests_html import HTML
from fake_useragent import UserAgent
from concurrent.futures import ThreadPoolExecutor, as_completed

def create_driver():
    useragent = UserAgent()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f"user-agent={useragent.random}")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")

    return webdriver.Chrome(options=chrome_options)

def extract_product_details(html_object):
    product_details = {
        'title': html_object.find('h1', first=True).text if html_object.find('h1', first=True) else 'No Title Found',
        'description': html_object.find('div.markup', first=True).text if html_object.find('div.markup', first=True) else 'No Description Found',
        'features': [feature.text for feature in html_object.find('ul li')] if html_object.find('ul li') else 'No Features Found',
    }
    return product_details

def click_see_all_button(driver):
    try:
        see_all_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/catalog/productratingsreviews/sku/']"))
        )
        href = see_all_button.get_attribute('href')
        return href if href.startswith('http') else "https://www.jumia.co.ke" + href
    except (NoSuchElementException, TimeoutException):
        return None

def extract_reviews(driver):
    reviews_data = []
    try:
        reviews = driver.find_elements(By.CSS_SELECTOR, "article")
        for review in reviews:
            try:
                rating = review.find_element(By.CSS_SELECTOR, ".stars").text.split(" ")[0]
                title = review.find_element(By.CSS_SELECTOR, "h3").text
                body = review.find_element(By.CSS_SELECTOR, "p").text
                reviews_data.append({"rating": rating, "title": title, "body": body})
            except NoSuchElementException:
                continue
    except Exception as e:
        return []
    return reviews_data

def fetch_page_reviews(driver, review_url, page_number):
    try:
        driver.get(f"{review_url}?page={page_number}")
        return extract_reviews(driver)
    except Exception as e:
        return []

def extract_all_reviews(driver, url):
    driver.get(url)
    review_url = click_see_all_button(driver)
    
    if not review_url:
        return []

    all_reviews = extract_reviews(driver)

    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = {executor.submit(fetch_page_reviews, driver, review_url, page): page for page in range(2, 6)}
        
        for future in as_completed(futures):
            page_reviews = future.result()
            if not page_reviews:
                break
            all_reviews.extend(page_reviews)

    return all_reviews

def get_jumia_product_info(url: str):
    driver = create_driver()
    try:
        driver.get(url)
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.row")))

        html_str = driver.page_source
        html_object = HTML(html=html_str)

        product_details = extract_product_details(html_object)
        reviews = extract_all_reviews(driver, url)

        return {"product_details": product_details, "reviews": reviews if reviews else "No reviews found."}
    
    except Exception as e:
        return {"error": str(e), "message": "Error occurred while fetching the product details and reviews."}
    
    finally:
        driver.quit()
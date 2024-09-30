from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from fake_useragent import UserAgent
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# Set up ChromeOptions for faster execution
useragent = UserAgent()
random_useragent = useragent.random

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f"user-agent={random_useragent}")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--blink-settings=imagesEnabled=false")  # Disable image loading to save bandwidth

# Initialize WebDriver globally for reuse
driver = webdriver.Chrome(options=chrome_options)

def click_see_all_button(driver):
    try:
        # Reduced timeout to speed up failure detection
        see_all_button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/catalog/productratingsreviews/sku/']"))
        )
        href = see_all_button.get_attribute('href')
        full_link = href if href.startswith('http') else "https://www.jumia.co.ke" + href
        driver.get(full_link)
        return full_link
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
                date_user = review.find_element(By.CSS_SELECTOR, ".-pvs").text
                reviews_data.append({"rating": rating, "title": title, "body": body, "date_user": date_user})
            except NoSuchElementException:
                continue
    except Exception as e:
        print(f"Error extracting reviews: {e}")
    return reviews_data

def fetch_page_reviews(review_url, page_number):
    try:
        driver.get(f"{review_url}?page={page_number}")
        return extract_reviews(driver)
    except Exception as e:
        return []

def extract_all_reviews(url):
    driver.get(url)
    review_url = click_see_all_button(driver)
    
    if not review_url:
        return []

    all_reviews = extract_reviews(driver)

    # Parallel processing of additional pages
    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = {executor.submit(fetch_page_reviews, review_url, page): page for page in range(2, 6)}
        
        for future in as_completed(futures):
            page_reviews = future.result()
            if not page_reviews:
                break
            all_reviews.extend(page_reviews)

    driver.quit()
    return all_reviews

def get_jumia_comments(url: str):
    try:
        reviews = extract_all_reviews(url)
        return {"message": "No reviews found."} if not reviews else reviews
    except Exception as e:
        return {"error": str(e), "message": "Error occurred while fetching the reviews."}

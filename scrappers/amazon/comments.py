from fake_useragent import UserAgent
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
import time

# Function to initialize the WebDriver with interceptor and options
def initialize_driver():
    useragent = UserAgent()
    random_useragent = useragent.random

    def interceptor(request):
        request.headers["Accept-Language"] = "en-US,en;q=0.9"
        request.headers["Referer"] = "https://www.google.com/"
        request.headers["User-Agent"] = random_useragent

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    driver.request_interceptor = interceptor
    return driver

# Function to extract comments from the current page
def get_comments_on_page(driver):
    comments = []
    try:
        comment_elements = driver.find_elements(By.CSS_SELECTOR, 'div[data-hook="review"]')
        if not comment_elements:
            return comments

        for comment in comment_elements:
            try:
                review_text = comment.find_element(By.CSS_SELECTOR, 'span[data-hook="review-body"]').text
                comments.append(review_text)
            except NoSuchElementException:
                pass

    except NoSuchElementException:
        pass
    
    return comments

# Function to click "Next" button and iterate over pages with a limit
def click_next_button_until_last(driver, max_pages=10):
    all_comments = []
    page_number = 1

    while page_number <= max_pages:
        try:
            comments = get_comments_on_page(driver)
            all_comments.extend(comments)

            # Find and click the "Next" button
            next_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'li.a-last a'))
            )
            next_button.click()
            time.sleep(3)  # Wait for the next page to load
            page_number += 1
            
        except (NoSuchElementException, TimeoutException):
            break

    return all_comments

# Function to click "See More Reviews" and start scraping comments
def click_see_more_reviews(driver):
    try:
        see_more_reviews_link = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-hook="see-all-reviews-link-foot"]'))
        )
        href_link = see_more_reviews_link.get_attribute("href")

        # Build full URL for reviews if needed
        full_url = "https://www.amazon.com" + href_link if href_link.startswith("/") else href_link
        driver.get(full_url)
        time.sleep(3)  # Wait for the reviews page to load

        all_comments = click_next_button_until_last(driver)
        return all_comments

    except NoSuchElementException:
        pass
    
    return []

def get_comments(url: str):
    driver = initialize_driver()

    try:
        driver.get(url)
        time.sleep(3)  # Wait for the page to load

        # Check if the page loaded successfully or if there's an error (e.g., 404)
        if "Page Not Found" in driver.page_source or driver.title == "404 - Page Not Found":
            raise WebDriverException("Invalid URL or Page not found.")

        # Try to navigate to the reviews and scrape comments
        all_comments = click_see_more_reviews(driver)

        return all_comments

    except TimeoutException:
        raise WebDriverException("Timeout occurred while loading the page.")
    except WebDriverException as e:
        raise e
    finally:
        driver.quit()

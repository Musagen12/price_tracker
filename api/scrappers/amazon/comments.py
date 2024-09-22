import logging
from fake_useragent import UserAgent
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
import time

# Setup logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()  # This will output logs to the console
    ]
)

# Function to initialize the browser with custom settings
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
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--enable-logging")
    chrome_options.add_argument("--v=1")

    driver = webdriver.Chrome(options=chrome_options)
    driver.request_interceptor = interceptor
    
    logging.info("Driver initialized with random user agent.")
    return driver

# Function to scrape comments from a single page
def get_comments_on_page(driver):
    comments = []
    try:
        comment_elements = driver.find_elements(By.CSS_SELECTOR, 'div[data-hook="review"]')
        if not comment_elements:
            logging.warning("No comments found on this page.")
            return comments

        for comment in comment_elements:
            try:
                review_text = comment.find_element(By.CSS_SELECTOR, 'span[data-hook="review-body"]').text
                comments.append(review_text)
                logging.debug(f"Scraped comment: {review_text}")
            except StaleElementReferenceException:
                logging.warning("Stale element reference. Skipping this comment.")

    except NoSuchElementException:
        logging.error("No comments found on this page.")
    
    return comments

# Function to navigate through pages and scrape comments
def click_next_button_until_last(driver):
    all_comments = []
    page_number = 1
    while True:
        try:
            # Get comments from the current page
            comments = get_comments_on_page(driver)
            all_comments.extend(comments)
            logging.info(f"Page {page_number} - Retrieved {len(comments)} comments.")

            # Find and click the 'Next' button to go to the next page
            next_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'li.a-last a'))
            )
            
            logging.info(f"Page {page_number} - Clicking 'Next' button.")
            next_button.click()
            time.sleep(3)  # Wait for the next page to load
            page_number += 1
            
        except (NoSuchElementException, TimeoutException):
            logging.info(f"Page {page_number} - No 'Next' button found. Reached the last page or timeout occurred.")
            break
        except Exception as e:
            logging.error(f"An error occurred on page {page_number}: {e}")
            break

    return all_comments

# Function to click on "See More Reviews" and start navigating pages
def click_see_more_reviews(driver):
    try:
        see_more_reviews_link = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-hook="see-all-reviews-link-foot"]'))
        )
        href_link = see_more_reviews_link.get_attribute("href")
        logging.info(f"Found 'See more reviews' link: {href_link}")

        full_url = "https://www.amazon.com" + href_link if href_link.startswith("/") else href_link
        logging.info(f"Navigating to: {full_url}")
        driver.get(full_url)
        time.sleep(3)  # Wait for the reviews page to load

        # Scrape comments from all the pages
        all_comments = click_next_button_until_last(driver)
        return all_comments

    except NoSuchElementException:
        logging.error("No 'See more reviews' link found.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    
    return []

# Main function to start the scraping process
def get_comments(url: str):
    driver = initialize_driver()

    try:
        driver.get(url)
        time.sleep(3)  # Wait for the page to load

        # Try to navigate to the reviews and scrape comments
        all_comments = click_see_more_reviews(driver)
        time.sleep(5)

        logging.info(f"Total comments scraped: {len(all_comments)}")
        return all_comments

    finally:
        driver.quit()

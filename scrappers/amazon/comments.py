from fake_useragent import UserAgent
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
import time

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

def get_comments(driver):
    try:
        comments = driver.find_elements(By.CSS_SELECTOR, 'div[data-hook="review"]')
        if not comments:
            print("No comments found on this page.")
        for comment in comments:
            try:
                review_text = comment.find_element(By.CSS_SELECTOR, 'span[data-hook="review-body"]').text
                print(review_text)
                print("=" * 50)
            except StaleElementReferenceException:
                print("Stale element reference. Skipping this comment.")
    except NoSuchElementException:
        print("No comments found.")

def click_next_button_until_last(driver):
    page_number = 1
    while True:
        try:
            get_comments(driver)
            print(f"Page {page_number} - Getting comments.")

            next_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'li.a-last a'))
            )
            
            print(f"Page {page_number} - Clicking 'Next' button.")
            next_button.click()
            time.sleep(3)  # Wait for the next page to load
            page_number += 1
            
        except (NoSuchElementException, TimeoutException):
            print(f"Page {page_number} - No 'Next' button found. Reached the last page or timeout occurred.")
            break
        except Exception as e:
            print(f"An error occurred on page {page_number}: {e}")
            break

def click_see_more_reviews(driver):
    try:
        see_more_reviews_link = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-hook="see-all-reviews-link-foot"]'))
        )
        href_link = see_more_reviews_link.get_attribute("href")
        print(f"Found 'See more reviews' link: {href_link}")

        full_url = "https://www.amazon.com" + href_link if href_link.startswith("/") else href_link
        print(f"Navigating to: {full_url}")
        driver.get(full_url)
        time.sleep(3)  # Wait for the reviews page to load

        click_next_button_until_last(driver)
    except NoSuchElementException:
        print("No 'See more reviews' link found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def get_comments(url: str):
    driver.get(url)
    time.sleep(3)  # Wait for the page to load

    click_see_more_reviews(driver)
    time.sleep(5)

    driver.quit()

get_amazon_comments(url="https://www.amazon.com/dp/B0D8L1RLD5")
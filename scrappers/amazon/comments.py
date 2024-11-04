from fake_useragent import UserAgent
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
import time
from requests_html import HTML

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
    chrome_options.page_load_strategy = 'eager'
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    driver.request_interceptor = interceptor
    return driver

# Function to extract product description/features
def extract_product_description(html_object):
    html = HTML(html=html_object)  # Parse the HTML content
    features = html.find('ul.a-unordered-list.a-vertical.a-spacing-mini li.a-spacing-mini')

    extracted_data = []
    for feature in features:
        feature_text = feature.text
        extracted_data.append(feature_text)
    
    return extracted_data

# Function to extract comments from the current page
def get_comments_on_page(driver):
    comments = []
    try:
        comment_elements = WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-hook="review"]'))
        )
        for comment in comment_elements:
            try:
                review_text = comment.find_element(By.CSS_SELECTOR, 'span[data-hook="review-body"]').text
                comments.append(review_text)
            except NoSuchElementException:
                continue
    except TimeoutException as e:
        print(f"Timeout while trying to get comments: {e}")
    
    return comments

def click_next_button_until_last(driver, max_pages=10):
    all_comments = []
    page_number = 1

    while page_number <= max_pages:
        try:
            comments = get_comments_on_page(driver)
            all_comments.extend(comments)

            # Check if the "Next" button is present
            next_button = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'li.a-last a'))
            )
            
            if next_button and next_button.is_displayed() and next_button.is_enabled():
                print(f"Navigating to page {page_number + 1}...")

                # Click the "Next" button and wait for new reviews to load
                next_button.click()
                time.sleep(5)  # Delay to simulate human interaction

                # Wait for the new comments to load
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-hook="review"]'))
                )

                page_number += 1
            else:
                print("No more pages to scrape.")
                break
            
        except TimeoutException as e:
            print(f"Timeout occurred on page {page_number}: {e}")
            print("There are no more pages to scrape.")
            break
        except NoSuchElementException:
            print("No 'Next' button found. Reached the last page.")
            print("There are no more pages to scrape.")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break

    return all_comments



# Function to click "See More Reviews" and start scraping comments
def click_see_more_reviews(driver):
    try:
        see_more_reviews_link = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-hook="see-all-reviews-link-foot"]'))
        )
        href_link = see_more_reviews_link.get_attribute("href")

        # Build full URL for reviews if needed
        full_url = "https://www.amazon.com" + href_link if href_link.startswith("/") else href_link
        driver.get(full_url)
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-hook="review"]')))

        all_comments = click_next_button_until_last(driver)
        return all_comments

    except NoSuchElementException:
        print("No 'See More Reviews' link found.")
    
    return []

# Main function to scrape product description and comments
def get_product_info_and_comments(url: str):
    driver = initialize_driver()

    try:
        driver.get(url)
        
        # Check if the page loaded successfully or if there's an error (e.g., 404)
        if "Page Not Found" in driver.page_source or driver.title == "404 - Page Not Found":
            raise WebDriverException("Invalid URL or Page not found.")

        # Extract the entire page's HTML content
        html_content = driver.page_source

        # Extract product description
        product_description = extract_product_description(html_content)

        # Navigate to the reviews and scrape comments
        all_comments = click_see_more_reviews(driver)

        # Return both product description and comments
        return {
            'product_description': product_description,
            'comments': all_comments
        }

    except TimeoutException as e:
        print(f"Timeout occurred: {e}")
        raise WebDriverException("Timeout occurred while loading the page.")
    except WebDriverException as e:
        print(f"WebDriverException: {e}")
        raise e
    finally:
        driver.quit()

# # Example usage:
# product_info = get_product_info_and_comments("https://www.amazon.com/dp/B01H6GUCCQ")
# print(product_info)

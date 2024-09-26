from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from fake_useragent import UserAgent
import time

# Create a random user agent using Fake UserAgent
useragent = UserAgent()
random_useragent = useragent.random

# Set up ChromeOptions to include the random user-agent and other preferences
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f"user-agent={random_useragent}")  # Apply the random user agent
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--enable-logging")
chrome_options.add_argument("--headless")  # Optional: run Chrome in headless mode
chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Disable automation detection

# Initialize the WebDriver
driver = webdriver.Chrome(options=chrome_options)

def click_see_all_button(driver):
    try:
        # Wait for the "See More" link to appear and click it
        wait = WebDriverWait(driver, 10)
        see_all_button = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/catalog/productratingsreviews/sku/']"))
        )
        
        href = see_all_button.get_attribute('href')
        if href:
            full_link = href if href.startswith('http') else "https://www.jumia.co.ke" + href
            print(f"Found 'See More' link: {full_link}")
            
            # Navigate to the full review page
            driver.get(full_link)
            print("Navigated to the 'See More' page.")
            
            return full_link
        else:
            print("No 'href' attribute found for the 'See More' button.")
            return None
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Could not find the 'See More' button: {e}")
        return None

def extract_reviews(driver):
    # Extract all reviews on the page
    reviews = driver.find_elements(By.CSS_SELECTOR, "article")
    reviews_data = []
    for review in reviews:
        try:
            rating = review.find_element(By.CSS_SELECTOR, ".stars").text.split(" ")[0]  # Extract the rating
            title = review.find_element(By.CSS_SELECTOR, "h3").text  # Extract the review title
            body = review.find_element(By.CSS_SELECTOR, "p").text  # Extract the review body
            date_user = review.find_element(By.CSS_SELECTOR, ".-pvs").text  # Extract the date and user information
            review_data = {"rating": rating, "title": title, "body": body, "date_user": date_user}  # Store in dict
            reviews_data.append(review_data)
            # print(f"Rating: {rating}, Title: {title}, Review: {body}, Date/User: {date_user}")
        except NoSuchElementException:
            continue
    return reviews_data

def extract_all_reviews(url):
    driver.get(url)

    # Step 1: Click the "See More" button to go to the review section
    review_url = click_see_all_button(driver)
    
    if not review_url:
        print("Failed to navigate to the reviews section.")
        return []

    # To store reviews for comparison across pages
    all_reviews = []
    last_page_reviews = []

    # Step 2: Extract reviews from the first page
    current_page_reviews = extract_reviews(driver)
    all_reviews.extend(current_page_reviews)  # Add first page reviews

    # Step 3: Start looping through pages starting from page 2
    page_number = 2
    while True:
        try:
            # Construct the URL for the next page by appending `?page=page_number`
            next_page_url = f"{review_url}?page={page_number}"
            driver.get(next_page_url)
            print(f"Navigating to page {page_number} using URL pagination...")

            # Extract reviews on this page
            current_page_reviews = extract_reviews(driver)

            # Stop the loop if no new reviews are found or reviews start repeating
            if not current_page_reviews or current_page_reviews == last_page_reviews:
                print(f"No more new reviews or repetition detected on page {page_number}. Stopping.")
                break

            # Save the current page reviews for the next comparison
            last_page_reviews = current_page_reviews
            all_reviews.extend(current_page_reviews)  # Add reviews from the current page

            # Increment page number to move to the next page
            page_number += 1

        except (NoSuchElementException, TimeoutException):
            print(f"Error or no more pages after page {page_number}.")
            break

    driver.quit()
    return all_reviews  # Return all collected reviews

def get_jumia_comments(url: str):
    return extract_all_reviews(url)  # Return the reviews from the URL

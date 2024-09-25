from fake_useragent import UserAgent
from seleniumwire import webdriver
from requests_html import HTML

def get_random_useragent():
    useragent = UserAgent()
    return useragent.random

def setup_driver(random_useragent):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)

    def interceptor(request):
        request.headers["Accept-Language"] = "en-US,en;q=0.9"
        request.headers["Referer"] = "https://www.google.com/"
        request.headers["User-Agent"] = random_useragent

    driver.request_interceptor = interceptor
    return driver

def fetch_page_source(driver, url):
    try:
        driver.get(url)
        html_str = driver.page_source
        return html_str
    except Exception:
        return None
    finally:
        driver.quit()

def parse_html(html_str):
    return HTML(html=html_str) if html_str else None

def extract_product_data(html_object):
    try:
        name = html_object.find('#productTitle', first=True).text or "Name not available"
        picture = html_object.find("#landingImage", first=True)
        image_src = picture.attrs['src'] if picture else "No image available"
        stock_status = html_object.find("#availability", first=True)
        in_stock = stock_status.text.strip() if stock_status else "Not in stock"
        rating_element = html_object.find("#acrPopover", first=True)
        rating = rating_element.attrs['title'] if rating_element else "No rating available"
        
        return name, image_src, in_stock, rating
    except Exception:
        return "Error", "Error", "Error", "Error"

def extract_price_from_string(value: str):
    if isinstance(value, str):
        value = value.replace('$', '').replace(',', '').strip() 
        try:
            return float(value) if value else None
        except ValueError:
            return None
    return None

def extract_table_data(html_object):
    dataset = {}
    tables = html_object.find('table')

    for table in tables:
        for tbody in table.element.getchildren():
            for tr in tbody.getchildren():
                row = [col.text_content().strip() for col in tr.getchildren() if col.text_content()]
                if len(row) == 2:
                    key, value = row
                    key = key.replace("-", "_")
                    dataset[key] = value

    return dataset

def get_product_details(dataset):
    asin = dataset.get('ASIN', "ASIN not available")
    manufacturer = dataset.get('Manufacturer', "Manufacturer not available")
    
    total_price = dataset.get('Total', "$0.00")
    price = extract_price_from_string(str(total_price))

    return asin, manufacturer, price

def get_individual_amazon_item(url: str):
    random_useragent = get_random_useragent()
    driver = setup_driver(random_useragent)
    
    html_str = fetch_page_source(driver, url)
    html_object = parse_html(html_str)
    
    if html_object is None:
        return {"Error": "Failed to retrieve HTML"}

    name, image_src, in_stock, rating = extract_product_data(html_object)
    
    dataset = extract_table_data(html_object)
    asin, manufacturer, price = get_product_details(dataset)

    product_data = {
        "Product Name": name,
        "In Stock": in_stock,
        "Rating": rating,
        "Image Source": image_src,
        "Price": price,
        "Manufacturer": manufacturer,
        "ASIN": asin,
        "Product URL": f"https://www.amazon.com/dp/{asin}/"
    }

    return product_data

# product_info = get_individual_amazon_item(url="https://www.amazon.com/dp/B01H6GUCCQ/")
# print(product_info)

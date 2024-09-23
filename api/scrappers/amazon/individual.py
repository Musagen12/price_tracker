# # from fake_useragent import UserAgent
# # from seleniumwire import webdriver
# # from selenium.webdriver.common.by import By
# # from selenium.webdriver.common.keys import Keys
# # from requests_html import HTML
# # import re

# # useragent = UserAgent()

# # random_useragent = useragent.random
# # url = "https://www.amazon.com/dp/B098LG3N6R/"
# # # B098LG3N6R

# # print("pass")


# # def interceptor(request):
# #     request.headers["Accept-Language"] = "en-US,en;q=0.9"
# #     request.headers["Referer"] = "https://www.google.com/"
# #     request.headers["User-Agent"] = random_useragent

# # chrome_options = webdriver.ChromeOptions()
# # chrome_options.add_argument("--headless")

# # driver = webdriver.Chrome(options=chrome_options)

# # driver.request_interceptor = interceptor


# # driver.get(url=url)
# # html_str = driver.page_source
# # driver.quit()
# # html_object = HTML(html=html_str)


# # name = html_object.find('#productTitle', first=True).text
# # rating = html_object.find("#acrPopover", first=True)
# # picture = html_object.find("#landingImage", first=True)
# # src = picture.attrs['src']


# # def get_stock():
# #     in_stock = html_object.find("#availability", first=True).text
# #     return in_stock

# # base_stock = get_stock()

# # if base_stock is None:
# #     in_stock = "Not in stock"


# # def get_rating():
# #     rating = html_object.find("#acrPopover", first=True)
# #     return rating

# # base_rating = get_rating()

# # if base_rating is None:
# #     rating_final = "No rating is available"
# # else:
# #     rating_final = rating.attrs['title']


# # dataset = {}

# # tables = html_object.find('table')

# # def extract_price_from_string(value: str, regex=r"[\$]{1}[\d,]+\.?\d{0,2}"):
# #     x = re.findall(regex, value)
# #     val = None
# #     if len(x) == 1:
# #         val = x[0]
# #     return val

# # dataset = {}
# # for table in tables:
# #             for tbody in table.element.getchildren():
# #                 for tr in tbody.getchildren():
# #                     row = []
# #                     for col in tr.getchildren():
# #                         content = ""
# #                         try:
# #                             content = col.text_content()
# #                         except:
# #                             pass
# #                         if content != "":
# #                             _content = content.strip()
# #                             row.append(_content)
# #                     if len(row) != 2:
# #                         continue
# #                     key = row[0]
# #                     value = row[1]
# #                     data = {}
# #                     key = key.replace("-", "_")
# #                     if key in dataset:
# #                         continue
# #                     else:
# #                         if "$" in value:
# #                             new_key = key
# #                             old_key = f'{key}_raw'
# #                             new_value = extract_price_from_string(value)
# #                             old_value = value
# #                             dataset[new_key] = new_value
# #                             dataset[old_key] = old_value
# #                         else:
# #                             dataset[key] = value


# # if dataset['ASIN'] == None:
# #     asin = "Asin not vailable"
# # else:
# #     asin = dataset['ASIN']

# # if dataset['Manufacturer'] == None:
# #     manufacturer = "Manufacturer is not available."
# # else:
# #     manufacturer = dataset['Manufacturer']

# # if dataset['Total'] == None:
# #     total_price = "Total price not vailable"
# # else:
# #     total_price = dataset['Total']


# # url = f"https://www.amazon.com/dp/{asin}/"


# # print(name)
# # print(base_stock)
# # print(rating_final)
# # print(src)
# # print(total_price)
# # print(manufacturer)
# # print(asin)
# # print(url)

# from fake_useragent import UserAgent
# from seleniumwire import webdriver
# from selenium.webdriver.common.by import By
# from requests_html import HTML
# import re

# def get_random_useragent():
#     """Generate a random user-agent using fake_useragent."""
#     useragent = UserAgent()
#     return useragent.random

# def setup_driver(random_useragent):
#     """Setup Chrome WebDriver with options and user-agent."""
#     chrome_options = webdriver.ChromeOptions()
#     chrome_options.add_argument("--headless")
#     chrome_options.add_argument("--disable-gpu")
#     chrome_options.add_argument("--no-sandbox")
#     chrome_options.add_argument("--disable-dev-shm-usage")
    
#     driver = webdriver.Chrome(options=chrome_options)

#     def interceptor(request):
#         request.headers["Accept-Language"] = "en-US,en;q=0.9"
#         request.headers["Referer"] = "https://www.google.com/"
#         request.headers["User-Agent"] = random_useragent

#     driver.request_interceptor = interceptor
#     return driver

# def fetch_page_source(driver, url):
#     """Fetch the page source HTML from the given URL."""
#     driver.get(url)
#     html_str = driver.page_source
#     driver.quit()
#     return html_str

# def parse_html(html_str):
#     """Parse HTML string using requests_html to extract HTML object."""
#     return HTML(html=html_str)

# def extract_product_data(html_object):
#     """Extract name, rating, image source, stock status, and other product details."""
#     name = html_object.find('#productTitle', first=True).text if html_object.find('#productTitle', first=True) else "Name not available"
    
#     picture = html_object.find("#landingImage", first=True)
#     image_src = picture.attrs['src'] if picture else "No image available"
    
#     stock_status = html_object.find("#availability", first=True)
#     in_stock = stock_status.text.strip() if stock_status else "Not in stock"
    
#     rating_element = html_object.find("#acrPopover", first=True)
#     rating = rating_element.attrs['title'] if rating_element else "No rating available"
    
#     return name, image_src, in_stock, rating

# def extract_price_from_string(value: str, regex=r"[\$]{1}[\d,]+\.?\d{0,2}"):
#     """Extract the price from a string based on a regular expression."""
#     x = re.findall(regex, value)
#     return x[0] if len(x) == 1 else None

# def extract_table_data(html_object):
#     """Extract product data from HTML table elements."""
#     dataset = {}
#     tables = html_object.find('table')

#     for table in tables:
#         for tbody in table.element.getchildren():
#             for tr in tbody.getchildren():
#                 row = [col.text_content().strip() for col in tr.getchildren() if col.text_content()]
#                 if len(row) == 2:
#                     key, value = row
#                     key = key.replace("-", "_")
#                     if "$" in value:
#                         new_value = extract_price_from_string(value)
#                         dataset[key] = new_value or value
#                     else:
#                         dataset[key] = value

#     return dataset

# def get_product_details(dataset):
#     """Retrieve ASIN, manufacturer, and total price from dataset."""
#     asin = dataset.get('ASIN', "ASIN not available")
#     manufacturer = dataset.get('Manufacturer', "Manufacturer not available")
#     total_price = dataset.get('Total', "Total price not available")
#     return asin, manufacturer, total_price

# def get_individual_amazon_item(url: str):
#     random_useragent = get_random_useragent()

#     driver = setup_driver(random_useragent)
#     html_str = fetch_page_source(driver, url)

#     html_object = parse_html(html_str)

#     name, image_src, in_stock, rating = extract_product_data(html_object)
    
#     dataset = extract_table_data(html_object)
#     asin, manufacturer, total_price = get_product_details(dataset)

#     print(f"Product Name: {name}")
#     print(f"In Stock: {in_stock}")
#     print(f"Rating: {rating}")
#     print(f"Image Source: {image_src}")
#     print(f"Total Price: {total_price}")
#     print(f"Manufacturer: {manufacturer}")
#     print(f"ASIN: {asin}")
#     print(f"Product URL: https://www.amazon.com/dp/{asin}/")

# get_individual_amazon_item(url="https://www.amazon.com/dp/B098LG3N6R/")
from fake_useragent import UserAgent
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from requests_html import HTML
import re

def get_random_useragent():
    """Generate a random user-agent using fake_useragent."""
    useragent = UserAgent()
    return useragent.random

def setup_driver(random_useragent):
    """Setup Chrome WebDriver with options and user-agent."""
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
    """Fetch the page source HTML from the given URL."""
    driver.get(url)
    html_str = driver.page_source
    driver.quit()
    return html_str

def parse_html(html_str):
    """Parse HTML string using requests_html to extract HTML object."""
    return HTML(html=html_str)

def extract_product_data(html_object):
    """Extract name, rating, image source, stock status, and other product details."""
    name = html_object.find('#productTitle', first=True).text if html_object.find('#productTitle', first=True) else "Name not available"
    
    picture = html_object.find("#landingImage", first=True)
    image_src = picture.attrs['src'] if picture else "No image available"
    
    stock_status = html_object.find("#availability", first=True)
    in_stock = stock_status.text.strip() if stock_status else "Not in stock"
    
    rating_element = html_object.find("#acrPopover", first=True)
    rating = rating_element.attrs['title'] if rating_element else "No rating available"
    
    return name, image_src, in_stock, rating

def extract_price_from_string(value: str, regex=r"[\$]{1}[\d,]+\.?\d{0,2}"):
    """Extract the price from a string based on a regular expression."""
    x = re.findall(regex, value)
    return x[0] if len(x) == 1 else None

def extract_table_data(html_object):
    """Extract product data from HTML table elements."""
    dataset = {}
    tables = html_object.find('table')

    for table in tables:
        for tbody in table.element.getchildren():
            for tr in tbody.getchildren():
                row = [col.text_content().strip() for col in tr.getchildren() if col.text_content()]
                if len(row) == 2:
                    key, value = row
                    key = key.replace("-", "_")
                    if "$" in value:
                        new_value = extract_price_from_string(value)
                        dataset[key] = new_value or value
                    else:
                        dataset[key] = value

    return dataset

def get_product_details(dataset):
    """Retrieve ASIN, manufacturer, and total price from dataset."""
    asin = dataset.get('ASIN', "ASIN not available")
    manufacturer = dataset.get('Manufacturer', "Manufacturer not available")
    total_price = float(dataset.get('Total'))
    return asin, manufacturer, total_price

def get_individual_amazon_item(url: str):
    random_useragent = get_random_useragent()

    driver = setup_driver(random_useragent)
    html_str = fetch_page_source(driver, url)

    html_object = parse_html(html_str)

    name, image_src, in_stock, rating = extract_product_data(html_object)
    
    dataset = extract_table_data(html_object)
    asin, manufacturer, total_price = get_product_details(dataset)

    product_data = {
        "Product Name": name,
        "In Stock": in_stock,
        "Rating": rating,
        "Image Source": image_src,
        "Total Price": total_price,
        "Manufacturer": manufacturer,
        "ASIN": asin,
        "Product URL": f"https://www.amazon.com/dp/{asin}/"
    }

    return product_data

# product_info = get_individual_amazon_item(url="https://www.amazon.com/dp/B098LG3N6R/")


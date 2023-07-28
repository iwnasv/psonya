import json
import os
import sys
from bs4 import BeautifulSoup
from selenium import webdriver

#TODO: 1) cache ALL product codes and names into a JSON periodically,
#TODO: 2) something you can call dynamically like:
#         /api/product?id=1143
#         rather than hard-coded values

# Integers representing products
product_codes = [121, 1191, 1182, 427, 1143, 932, 55]

class Product:
    def __init__(self, code, name, price, store): #TODO: add image
        self.name = name
        self.code = code
        self.price = price
        self.store = store

# This array will contain product objects and eventually be JSON formatted
products = []

# CHROME BEGINS HERE
chrome_options = webdriver.ChromeOptions()
# Don't open browser window
chrome_options.add_argument("--headless")
# TODO: it's hard coded...
chrome_options.binary_location = r"C:\Users\iwnaras\Downloads\chrome-win64\chrome.exe"

# Redirect clutter to os.devnull
# Yes it's clutter. We only want the JSON response. Chrome will whine about javascipt.
sys.stdout = open(os.devnull, 'w')
sys.stderr = open(os.devnull, 'w')

# Bonus attempt to make Chrome chill out a bit
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

# Create the Chrome WebDriver
driver = webdriver.Chrome(options=chrome_options)
# CHROME ENDS HERE

# This is the good bit
for product_code in product_codes:
    url = f"https://e-katanalotis.gov.gr/product/{product_code}"

    driver.get(url)

    # Finally get actual js-rendered source
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    name_element = soup.find('p', {'class': 'product-name'})
    name = name_element.text if name_element else "Product not found"
    price_element = soup.find('span', {'class': 'product-price-number'})
    price = price_element.text if price_element else "Price N/A"
    store_element = soup.find('span', {'class': 'product-market-name'})
    store = store_element.text if store_element else "Store N/A"

    prod = Product(product_code, name, price, store)
    products.append(prod)

# Bye-bye Chrome WebDriver
driver.quit()

# Restore output now, because it's no longer Chrome's sob story
sys.stdout = sys.__stdout__
sys.stderr = sys.__stderr__

# Needs ensure_ascii=False
response = json.dumps([obj.__dict__ for obj in products], ensure_ascii=False, separators=(',', ':'))
print(response)

from bs4 import BeautifulSoup
from selenium import webdriver
import os

class ProductFetcher:
    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.chrome_options.add_argument("--disable-logging")
        self.chrome_options.add_argument("--log-level=0")

        if os.name == "posix":
            executable = "/usr/bin/chromium"
        else:
            executable = r"C:\Users\iwnaras\Downloads\chrome-win64\chrome.exe"
        self.chrome_options.binary_location = executable

        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.product_data = {}
        self.i = 0 # disassociate product code from array index

    def fetch_product_data(self, product_id):
        url = f"https://e-katanalotis.gov.gr/product/{product_id}"
        self.driver.get(url)
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        name_element = soup.find('p', {'class': 'product-name'})
        name = name_element.text if name_element else None
        price_element = soup.find('span', {'class': 'product-price-number'})
        price = price_element.text if price_element else None
        store_element = soup.find('span', {'class': 'product-market-name'})
        store = store_element.text if store_element else None
        pic_element = soup.find('img', {'class': 'product-img'})
        pic = pic_element['src'] if pic_element else None

        # If any of the essential attributes are "N/A", return None
        if name is not None or price is not None or store is not None:
            self.product_data[self.i] = {
                "code": product_id,
                "name": name,
                "price": price,
                "store": store,
                "pic": pic
            }
            self.i += 1

    def close(self):
        self.driver.quit()

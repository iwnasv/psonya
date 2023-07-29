import json
from fetch_product import ProductFetcher

# Product count changes, it's 1354 now. Find out the fun way, manually...
product_codes = list(range(1, 1354))

class Product:
    def __init__(self, code, name, price, store, pic):
        self.code = code
        self.name = name
        self.price = price
        self.store = store
        self.pic = pic

# This array will contain product objects and eventually be JSON formatted
products = []
fetcher = ProductFetcher()

for product_code in product_codes:
    fetcher.fetch_product_data(product_code)

    # Skip creating an object with unavailable values
    if fetcher.product_data[product_code] is None:
        continue

    prod = Product(**fetcher.product_data[product_code])
    products.append(prod)

    # Prevent overload and possible blacklisting
    # time.sleep(1)
fetcher.close()

output_file="products.json"
# Needs ensure_ascii=False
with open(output_file, "w", encoding="utf-8") as file:
    json.dump([obj.__dict__ for obj in products], file, ensure_ascii=False, separators=(',', ':'))

print(f"Data written to {output_file}")

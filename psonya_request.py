import hashlib
from flask import Flask, request, jsonify
import sys
import json
from fetch_product import ProductFetcher

app = Flask(__name__)

API_KEY_HASH = 'ab8406e9fe6dbd38611d816c4c18ee20c616023c13036e9d85eb2946be899760'

class Product:
    def __init__(self, code, name, price, store, pic):
        self.name = name
        self.code = code
        self.price = price
        self.store = store
        self.pic = pic

@app.route('/products', methods=['GET'])
def get_product():
    # Get the product ID and API key from the query parameters
    product_id = request.args.get('id', type=int)
    api_key = request.args.get('key')

    # Check if the API key is provided and valid
    if api_key is None:
        return jsonify({"error": "API key not provided."}), 400

    # Compare the hash
    if hashlib.sha256(api_key.encode()).hexdigest() != API_KEY_HASH:
        return jsonify({"error": "Invalid API key."}), 403

    if '-x' in sys.argv:
        fetcher = ProductFetcher()
        product_data = fetcher.fetch_product_data(product_id)
        fetcher.close()
        if product_data is None:
            return jsonify({"error": "Product not found."}), 404

        response = jsonify(product_data)
        return response

    else:
        if product_id is None:
            # Read and return the whole JSON file
            with open('products.json', 'r') as json_file:
                data = json.load(json_file)
            return jsonify(data)

        with open('products.json', 'r') as json_file:
            data = json.load(json_file)

        product = next((item for item in data if item['code'] == product_id), None)
        if product is None:
            return jsonify({"error": "Product not found."}), 404

        return jsonify(product)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')

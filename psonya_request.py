from flask import Flask, request, jsonify
import json
import sys
from fetch_product import ProductFetcher

app = Flask(__name__)

class Product:
    def __init__(self, code, name, price, store, pic):
        self.name = name
        self.code = code
        self.price = price
        self.store = store
        self.pic = pic

@app.route('/api', methods=['GET'])
def get_product():
    # Get the product ID from the query parameters
    product_id = request.args.get('id', type=int)

    # Check if the ID is valid
    if product_id is None:
        return jsonify({"error": "Product ID not provided."}), 400

    if '-x' in sys.argv:
        fetcher = ProductFetcher()
        product_data = fetcher.fetch_product_data(product_id)
        fetcher.close()
        if product_data is None:
            return jsonify({"error": "Product not found."}), 404

        response = json.dumps(product_data, ensure_ascii=False, separators=(',', ':'))
        return app.response_class(response, content_type='application/json')

    else:
        with open('products.json', 'r') as json_file:
            data = json.load(json_file)

        product = next((item for item in data if item['code'] == product_id), None)
        if product is None:
            return jsonify({"error": "Product not found."}), 404

        return jsonify(product)

if __name__ == '__main__':
    app.run(debug=True)

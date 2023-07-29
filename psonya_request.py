from flask import Flask, request, jsonify
from fetch_product import ProductFetcher

app = Flask(__name__)

class Product:
    def __init__(self, code, name, price, store, pic):
        self.name = name
        self.code = code
        self.price = price
        self.store = store
        self.pic = pic

@app.route('/products', methods=['GET'])
def get_product():
    # Get the product ID from the query parameters
    product_id = request.args.get('id', type=int)

    # Check if the ID is provided and valid
    if product_id is None:
        return jsonify({"error": "Product ID not provided."}), 400

    fetcher = ProductFetcher()
    product_data = fetcher.fetch_product_data(product_id)
    fetcher.close()

    if product_data is None:
        return jsonify({"error": "Product not found."}), 404

    response = jsonify(product_data)
    return response

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1')

#  NGINX:
# location /products {
#     proxy_pass http://127.0.0.1:5000;
#     proxy_set_header Host $host;
#     proxy_set_header X-Real-IP $remote_addr;
# }
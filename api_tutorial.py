from flask import Flask, request, jsonify
import json

"""
Create a json file named "kbl_stocks.json" with below
[
    {
        "White Cap Can 500ml Local": "672419"
    },
    {
        "Senator Dark 50L": "688295"
    }
]
"""

app = Flask(__name__)

# Load the initial data from the JSON file
kbl_stocks = []  # our file is a json file of class type list


def load_kbl_stocks():
    try:
        with open('kbl_stocks.json', 'r') as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return []


def save_kbl_stocks(data):
    with open('kbl_stocks.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)  # indentation of 4 spaces for each level of nesting


# Route to get all kbl_stocks
@app.route('/api_tutorial/kbl_stocks', methods=['GET'])
def get_kbl_stocks():
    stocks = load_kbl_stocks()
    return jsonify(stocks)


# Route to serve the HTML form for adding stocks via a webpage
@app.route('/api_tutorial/kbl_stocks/add_stock_form', methods=['GET'])
def add_stock_form():
    return app.send_static_file('add_stock_form.html')


# Route to add stocks via query parameters. You can send the query directed as url e.g
# http://localhost:5001/api_tutorial/kbl_stocks/add_stock?material_description=White+Cap+Can+500ml+Local&material_code=672419
@app.route('/api_tutorial/kbl_stocks/add_stock', methods=['GET'])
def add_stock_via_query_parameters():
    material_description = request.args.get('material_description')
    material_code = request.args.get('material_code')

    if not material_description or not material_code:
        return jsonify({"error": "Both 'material_description' and 'material_code' query parameters are required"}), 400

    # Check if the material_description already exists in kbl_stocks
    for stock in kbl_stocks:
        if material_description in stock:
            return jsonify({"error": f"Stock with material description '{material_description}' already exists"}), 400

    # Create a new stock item with the product name as the key and the product code as the value
    new_stock = {
        material_description: material_code
    }

    # Append the new stock item to the list of stocks
    kbl_stocks.append(new_stock)

    # Optionally, you can save the updated stocks list to a file here
    save_kbl_stocks(kbl_stocks)

    # Create an HTML response with the heading and JSON data
    html_response = f"<h1>Added Stocks</h1><pre>{json.dumps(kbl_stocks, indent=4)}</pre>"

    # Return the HTML response
    return html_response, 201  # or you can just use "return jsonify(kbl_stocks), 201" to skip lines 74-78


# Route to serve the HTML form for deleting stocks via a webpage
@app.route('/api_tutorial/kbl_stocks/delete_stock_form', methods=['GET'])
def delete_stock_form():
    return app.send_static_file('delete_stock_form.html')


# Route to delete stocks via a POST request
@app.route('/api_tutorial/kbl_stocks/delete_stock', methods=['POST'])
def delete_stock():
    material_code = request.form.get('material_code')

    if not material_code:
        return jsonify({"error": "'material_code' form field is required"}), 400

    stocks = load_kbl_stocks()

    # Check if a stock item with the given material code exists
    for stock in stocks:
        if material_code in stock.values():
            # Remove the stock item from the list
            stocks.remove(stock)

            # Save the updated stocks back to the JSON file
            save_kbl_stocks(stocks)

            return jsonify({"message": f"Stock item with material code '{material_code}' deleted successfully"}), 200

    # If the stock item is not found, return an error response
    return jsonify({"error": f"Stock item with material code '{material_code}' not found"}), 404


if __name__ == '__main__':
    app.run(debug=True, port=5001)
import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import pandas as pd

# --- Flask App Initialization ---
# Point Flask to the 'frontend' folder for static files
app = Flask(__name__, static_folder='../frontend', static_url_path='/')
CORS(app)

# --- Data Loading ---

try:
    
    order_items_df = pd.read_csv('data/order_items.csv')
    products_df = pd.read_csv('data/products.csv')
    orders_df = pd.read_csv('data/orders.csv')
    inventory_items_df = pd.read_csv('data/inventory_items.csv')
    print("✅ Data loaded successfully!")
except FileNotFoundError as e:
    print(f"❌ Error loading data: {e}. Make sure the CSV files are in the 'backend/data/' directory.")
    exit()

# --- Logic Functions ---

def get_top_sold_products(limit=5):
    """Calculates the top N most sold products."""
    product_sales = order_items_df['product_id'].value_counts()
    top_products = product_sales.head(limit)
    top_products_df = top_products.reset_index()
    top_products_df.columns = ['product_id', 'sales_count']
    merged_df = pd.merge(
        top_products_df,
        products_df,
        left_on='product_id',
        right_on='id'
    )
    result = merged_df[['name', 'sales_count']]
    return result

def get_order_status(order_id):
    """Finds the status of a specific order by its ID."""
    order = orders_df[orders_df['order_id'] == order_id]
    if not order.empty:
        status = order['status'].iloc[0]
        return {"order_id": order_id, "status": status}
    else:
        return {"error": "Order not found"}

def get_stock_level(product_name):
    """
    Calculates the number of items in stock for a given product name.
    """
    in_stock_items = inventory_items_df[inventory_items_df['sold_at'].isnull()]
    stock_count = in_stock_items[in_stock_items['product_name'] == product_name].shape[0]
    return {"product_name": product_name, "stock_level": stock_count}


# --- API Endpoints ---

@app.route('/top_products', methods=['GET'])
def top_products_endpoint():
    """API endpoint to get the top 5 most sold products."""
    top_products = get_top_sold_products(limit=5)
    return jsonify(top_products.to_dict(orient='records'))

@app.route('/order_status/<int:order_id>', methods=['GET'])
def order_status_endpoint(order_id):
    """API endpoint to get the status of a specific order."""
    status = get_order_status(order_id)
    return jsonify(status)

@app.route('/stock_level', methods=['GET'])
def stock_level_endpoint():
    """API endpoint to get the stock level for a product."""
    product_name = request.args.get('product')
    if not product_name:
        return jsonify({"error": "Product name parameter is required"}), 400
    
    stock_info = get_stock_level(product_name)
    return jsonify(stock_info)

# --- Route to serve the frontend's main page ---
@app.route('/')
def serve_index():
    # The static_folder is '../frontend', so we serve index.html from there
    return send_from_directory(app.static_folder, 'index.html')


if __name__ == '__main__':
    # We run on 0.0.0.0 to be accessible from outside a Docker container
    app.run(host='0.0.0.0', port=5000, debug=True)
from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime
from collections import defaultdict

app = Flask(__name__)

# קריאת רשימת המוצרים מקובץ JSON
def load_products():
    with open('products.json', 'r', encoding='utf-8') as f:
        return json.load(f)['products']

# פונקציה לטעינת ההזמנות מקובץ JSON
def load_orders():
    if not os.path.exists('orders.json'):
        return []
    with open('orders.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        if not isinstance(data, dict) or 'orders' not in data:
            return []
        for order in data['orders']:
            order['order_items'] = order.pop('items', [])  # שינוי שם המפתח
        return data['orders']


# פונקציה לשמירת הזמנות לקובץ JSON
def save_order(order):
    orders = load_orders()
    orders.append(order)
    with open('orders.json', 'w', encoding='utf-8') as f:
        json.dump({"orders": orders}, f, ensure_ascii=False, indent=4)

@app.route('/')
def home():
    products = load_products()

    # קיבוץ מוצרים לפי קטגוריות
    categorized_products = defaultdict(list)
    for product in products:
        categorized_products[product["category"]].append(product)

    return render_template('index.html', categorized_products=categorized_products)

@app.route('/order', methods=['POST'])
def order():
    try:
        order_data = request.get_json()
        if not order_data:
            return jsonify({'error': 'Invalid JSON'}), 400

        # הוספת תאריך להזמנה
        order_data['order_date'] = datetime.now().strftime('%Y-%m-%d')

        # שמירת ההזמנה לקובץ JSON
        save_order(order_data)

        return jsonify({'message': 'ההזמנה נוספה בהצלחה!', 'order': order_data}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/orders')
def orders_page():
    orders = load_orders()
    return render_template('orders.html', orders=orders)



if __name__ == '__main__':
    app.run(debug=True)

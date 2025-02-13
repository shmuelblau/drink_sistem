from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime
from collections import defaultdict
import requests 


app = Flask(__name__)

def get_customer_id(email):
   
    api_token="78336597-A905-42AC-9A71-DC03B9A79647"
    url="https://api.rivhit.co.il/online/RivhitOnlineAPI.svc/Customer.Get"
    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "api_token": api_token,
        "email":email}
   
    response = requests.post(url, json=payload, headers=headers)
    response= response.json()
    customer_id=response["data"]["customer_id"]
    
    

    return customer_id

def send_order_to_rivhit(order_data):
   
    api_token="78336597-A905-42AC-9A71-DC03B9A79647"
    url = "https://api.rivhit.co.il/online/RivhitOnlineAPI.svc/Document.New"
    
  
    customer_id=get_customer_id(order_data["email"])
    
   



   
    payload = {
        "api_token": api_token,
        "document_type": 6,  # סוג המסמך (למשל חשבונית מס)
        "customer_id":customer_id ,  # ניתן לשנות אם יש לקוח רשום במערכת
        "email_to": order_data["email"],
        "email_dcc": order_data["email"],
        #"customer_create":True,
        #"mail_by_find":True,
        "items": [
            {
                "catalog_number": item["product_id"],
                "quantity": item["quantity"],
                "price_nis": item["price"]
            }
            for item in order_data["items"]
        ]
    }
   
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    print (response)
    return response.json()  # מחזיר את התגובה של ה-API



# קריאת רשימת המוצרים מקובץ JSON
def load_products():
    with open('products.json', 'r', encoding='utf-8') as f:
        return json.load(f)['products']




# פונקציה לשמירת הזמנות לקובץ JSON


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
       
        print(order_data)

        #יצירת הצעת מחיר 
        response = send_order_to_rivhit(order_data)

        return render_template('order.html',response=response)

    except Exception as e:
        return render_template('eror.html',response="נכשל")




if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime
from collections import defaultdict
import requests 


app = Flask(__name__)


def get_balance_for(email):

    try:
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
        balance = response["data"]["balance"]
            
            

           

        return balance
    
    except:
        return"לא ניתן להציג"


def get_customer_id(email):
   try:
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
   
   except:
       return 

def send_order_to_rivhit(order_data):
   
    api_token="78336597-A905-42AC-9A71-DC03B9A79647"
    url = "https://api.rivhit.co.il/online/RivhitOnlineAPI.svc/Document.New"
    
  
    customer_id=get_customer_id(order_data["email"])
    
    
   



   
    payload = {
        "api_token": api_token,
        "document_type": 4,  # סוג המסמך (למשל חשבונית מס)
        "customer_id":customer_id ,  # ניתן לשנות אם יש לקוח רשום במערכת
        "email_to": order_data["email"],
        "email_dcc": order_data["email"],
        #"customer_create":True,
        #"mail_by_find":True,
        "items": [
            {
                "item_id": item["product_id"],
                "quantity": item["quantity"],
                "price_nis": item["price"]
            }
            for item in order_data["items"]
        ]
    }
   
    headers = {
        "Content-Type": "application/json"
    }
    print(2)
    response = requests.post(url, json=payload, headers=headers)
    print(3)
    
    return response.json()  # מחזיר את התגובה של ה-API



# קריאת רשימת המוצרים מקובץ JSON
def load_products():
    with open('products.json', 'r', encoding='utf-8') as f:
        return json.load(f)['products']
# קריאת רשימת המוצרים מהתוכנה JSON
def products_from_rivhit():

    categories = {"מבצעים מיוחדים":11,"קוקה קולה": 1, "טמפו": 2,"בירה ויין":3,"משקאות אנרגיה":4,"מים":5,"שוופס":6,"פריגת ותפוזינה":7,"פיוז טי":8,"ספרינג":9,"ג'אמפ":10}
    items={}
    api_token="78336597-A905-42AC-9A71-DC03B9A79647"
    url = " https://api.rivhit.co.il/online/RivhitOnlineAPI.svc/Item.List"
    

    for category_name, category_id in categories.items():
        payload = {
            "api_token": api_token,
            "item_group_id": category_id
        }

        headers = {
            "Content-Type": "application/json"
        }

        respons = requests.post(url, json=payload, headers=headers).json()

        respons=respons['data']["item_list"]
        items[category_name]= respons
    print(items)
    
    return items 






@app.route('/')
def home():
    products = products_from_rivhit()

    # קיבוץ מוצרים לפי קטגוריות
    categorized_products = defaultdict(list)
  

    return render_template('index.html', categorized_products=products)

@app.route('/order', methods=['POST'])
def order():
    try:
        order_data = request.get_json()
        if not order_data:
            return jsonify({'error': 'Invalid JSON'}), 400

        
       
        print(order_data)

        #יצירת הצעת מחיר 
        response = send_order_to_rivhit(order_data)
        print(response)
        print(1)

        return render_template('order.html',response=response)

    except Exception as e:
        print(e)
        print(111111111111111)
        return render_template('eror.html',response="הזמנה נכשלה")

@app.route('/get_balance', methods=['POST'])
def get_balance():
    data = request.get_json()
    email = data.get('email')
    # כאן הקוד שלך שמחשב את היתרה, לדוגמה:
    balance = get_balance_for(email)
    return jsonify(balance=balance)


if __name__ == '__main__':
    app.run(debug=True)

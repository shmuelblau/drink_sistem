from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime
from collections import defaultdict
import requests 
def products_from_rivhit():
    api_token="78336597-A905-42AC-9A71-DC03B9A79647"
    url = " https://api.rivhit.co.il/online/RivhitOnlineAPI.svc/Item.List"
    

    payload = {
        "api_token": api_token,
        "item_group_id": 1
    }
   
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, json=payload, headers=headers).json()
    items=response['data']["item_list"]
    return items 
    
    

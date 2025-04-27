import time
import requests
import hmac
import hashlib
import os

API_KEY = os.getenv("XT_API_KEY")
API_SECRET = os.getenv("XT_API_SECRET")
BASE_URL = "https://www.xt.com"

def get_server_time():
    response = requests.get(f"{BASE_URL}/v4/public/time")
    return response.json()['result']

def sign_request(params, secret):
    sorted_params = sorted(params.items())
    message = '&'.join(f"{k}={v}" for k, v in sorted_params)
    signature = hmac.new(secret.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()
    return signature

def place_order():
    timestamp = get_server_time()
    params = {
        "symbol": "BTC_USDT",
        "side": "BUY",
        "type": "MARKET",
        "quantity": "0.001",
        "timestamp": timestamp
    }
    params['sign'] = sign_request(params, API_SECRET)

    headers = {
        "Content-Type": "application/json",
        "XT-API-KEY": API_KEY
    }

    response = requests.post(f"{BASE_URL}/v4/order", headers=headers, json=params)
    print(response.json())

if __name__ == "__main__":
    place_order()

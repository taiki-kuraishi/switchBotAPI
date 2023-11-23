import os
import time
import hashlib
import hmac
import base64
import json
import uuid
import requests
import json

# Create api header
def create_api_header(token:str, secret:str) -> dict:
    nonce = str(uuid.uuid4())
    t = int(round(time.time() * 1000))
    string_to_sign = '{}{}{}'.format(token, t, nonce)

    string_to_sign = bytes(string_to_sign, 'utf-8')
    secret = bytes(secret, 'utf-8')

    sign = base64.b64encode(
        hmac.new(secret, msg=string_to_sign, digestmod=hashlib.sha256).digest())

    apiHeader = {}
    apiHeader["Authorization"] = token
    apiHeader['Content-Type']='application/json'
    apiHeader['charset']='utf8'
    apiHeader["t"] = str(t)
    apiHeader["sign"] = str(sign, 'utf-8')
    apiHeader["nonce"] = nonce

    return apiHeader


token = os.environ['SWITCHBOT_TOKEN']
secret = os.environ['SWITCHBOT_SECRET']

apiHeader = create_api_header(token, secret)

response = requests.get(
    "https://api.switch-bot.com/v1.1/devices", headers=apiHeader)
devices = response.json()

# output json file
with open('../docs/devicesList.json', 'w', encoding='utf-8') as f:
    json.dump(devices, f, ensure_ascii=False)

print("Success get device list.")
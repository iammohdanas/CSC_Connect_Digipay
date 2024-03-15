import base64
import json
import os
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from datetime import datetime

APPNAME = 'DigiPay'

WAL_URL = 'http://10.1.82.165/'
WAL_CREDIT = 'digipay/credit'
url = WAL_URL + WAL_CREDIT
api_timeout = 90

def aes_encrypt(plain, key, a_key='J', enc_out='B64'):
    if a_key == 'J':
        plain = json.dumps(plain)
    
    method = AES.MODE_CBC
    aes_key = base64.b64decode(key)
    iv = os.urandom(16)
    cipher = AES.new(aes_key, method, iv)
    enc_int = cipher.encrypt(pad(plain.encode(), AES.block_size))
    enc_data = iv + enc_int
    
    if enc_out == 'HEX':
        enc_dat = enc_data.hex()
    elif enc_out == 'B64':
        enc_dat = base64.b64encode(enc_data).decode()
    
    return enc_dat

def aes_decrypt(cipher, key, ret='J', enc_in='B64'):
    enc = stat_split(cipher, enc_in)  # decode cipher
    aes_key = base64.b64decode(key)
    method = 'AES-256-CBC'
    cipher = AES.new(aes_key, AES.MODE_CBC, enc['iv'])
    dec_data = cipher.decrypt(enc['dat']).decode('utf-8').strip()
    
    if ret == 'J':
        return json.loads(dec_data)
    else:
        return dec_data

def stat_split(enc, enc_in):
    if enc_in == 'HEX':
        enc_dat = bytes.fromhex(enc)
    elif enc_in == 'B64':
        enc_dat = base64.b64decode(enc)

    iv = enc_dat[:16]
    dat = enc_dat[16:]
    
    return {'iv': iv, 'dat': dat}
payload = {
        'head': {
            'clientId': 'W01',
            'appName': APPNAME,
            'refId': '2302241653592001003000170157',
            'ts': datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
            'reqAction': 'credit',
            'clientIp': '127.0.0.1'
        },
        # request body
        'body': {
            'cscId': '200100300017',
            'dataSet': 'dgp',

            'txnDate': datetime.now().strftime('%Y-%m-%d'),
            
        }
    }
req_dat = {
        'clientId': 'W01',
        'reqData': payload
    }
payload = json.dumps(req_dat)
headers = {'Content-Type': 'application/json'}

response = requests.post(url, data=payload, headers=headers, timeout=api_timeout, verify=False)
response_json = response.text

print(response_json)
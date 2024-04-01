import random
import string
import base64
import os
from Crypto.Cipher import AES
import json
from Crypto.Util.Padding import pad, unpad

import requests

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
    cipher_aes = AES.new(aes_key, AES.MODE_CBC, enc['iv'])
    dec_data = unpad(cipher_aes.decrypt(enc['dat']), AES.block_size).decode('utf-8').strip()
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







def generate_key(length=64):
    characters = string.ascii_letters + string.digits
    key = ''.join(random.choice(characters) for _ in range(length))
    return key
    

key = generate_key(length=32)
print("generated key", key)

shift = 3
def encrypt_key(key, shift):
    encrypted_key = ''
    for char in key:
        if char.isalpha():
            if char.islower():
                encrypted_key += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            else:
                encrypted_key += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
        else:
            encrypted_key += char
    return encrypted_key

def decrypt_key(key, shift):
    decrypted_key = ''
    for char in key:
        if char.isalpha():
            if char.islower():
                decrypted_key += chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
            else:
                decrypted_key += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
        else:
            decrypted_key += char
    return decrypted_key

encrypted_key = encrypt_key(key,shift)
print('encrypted key : ',encrypted_key)
print('decrypted_key',decrypt_key(encrypted_key,shift))

def process_IBL_txn():
    data = {
        'Customerid': '123456789',
        'Transaction Type': 'DEBIT',
        'CustomerRefNumber': 'REF123',
        'DebitAccountNo': '1234567890123',
        'BeneficiaryName': 'John Doe',
        'CreditAccountNumber': '9876543210987',
        'BeneficiaryBankIFSCCode': 'INDU1234567',
        'TransactionAmount': '1000.00',
        'Beneficiary Mobile Number': '9876543210',
        'Email ID': 'john.doe@example.com',
        'Reserve1': '',
        'Reserve2': '',
        'Reserve3': '',
    }
    return data

# enc_data = aes_encrypt(process_IBL_txn(),key)
# print(enc_data)
json_data = process_IBL_txn()
json_encrypted_data = aes_encrypt(json_data,key)
print('encrypted json data',json_encrypted_data)
print('decrypted json data',aes_decrypt(json_encrypted_data,key))



data = {
    "data": json_encrypted_data,
    "key": encrypted_key,
    "bit": 0
}
api_timeout = 30
headers = {
    "IBL-Client-Id": "fce6de82afe45543d10849f5f3f6211c",
    "IBL-Client-Secret": "30777c257ddc85059a7b5cc459ff5f93",
    "Content-Type": "application/json"
}

process_txn_api_url = 'https://indusapiuat.indusind.com/indusapi-np/uat/sync-apis/ISync/ProcessTxn'
# response = requests.post(process_txn_api_url, json=data)
print(process_txn_api_url)
print(data)
print(headers)
response = requests.post(process_txn_api_url, json=data, headers=headers, timeout=api_timeout, verify=True)

print(response)
# decrypted_response = aes_decrypt(response, encrypted_key)



# print(aes_decrypt(enc_data,key))


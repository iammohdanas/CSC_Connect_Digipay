import random
import string
import base64
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import json

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


def generate_key(length=64):
    characters = string.ascii_letters + string.digits
    key = ''.join(random.choice(characters) for _ in range(length))
    return key

key = generate_key(length=32)

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

print(encrypt_key(key,shift))
import base64
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import json



class DataEncryption:
    def __init__(self,key):
        self.key=key
        self.iv=('0'*16).encode('utf-8')
    def encryptFun(self,reqData):
        try:
            cipher_encrypt = AES.new(self.key, AES.MODE_CBC,self.iv)
            ciphered_bytes = cipher_encrypt.encrypt(pad(reqData.encode('utf-8'),AES.block_size))
            # finalData=iv+ciphered_bytes
            finaData=self.iv+ciphered_bytes
            cipher_data = base64.b64encode(finaData)
            return cipher_data
        except:
            return None

    def decrptFun(self,cryptdata,flag=None):
            try:
                if type(cryptdata)==str:
                    cryptdata=cryptdata.encode('utf-8')
                ciphered_data = base64.b64decode(cryptdata)
                iv,data=ciphered_data[0:16],ciphered_data[16:]
                cipher_decrypt = AES.new(self.key, AES.MODE_CBC,iv=iv)
                deciphered_bytes = cipher_decrypt.decrypt(data)
                decrypted_data = deciphered_bytes.decode('windows-1252')
                if flag:
                    data=decrypted_data[:decrypted_data.rfind('|')]
                    return data
                else:
                    jsonData=json.loads(decrypted_data[:decrypted_data.rfind('}')+1])
                return jsonData
            except:
                jsonData=None
                return jsonData
            



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
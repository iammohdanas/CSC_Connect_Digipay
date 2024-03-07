import base64
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
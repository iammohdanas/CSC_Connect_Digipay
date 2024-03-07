import subprocess
import json
import random, os
from random import randint
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from binascii import hexlify

class Connect:
    def __init__(self,client_id, redirect_uri, client_key):
        self.base_url = "https://connectuat.csccloud.in/"
        self.key = client_key
        self.client_id = client_id
        self.redirect_uri = redirect_uri

    def _generate_random_number(self):
        return randint(10000, 99999)

    def _generate_iv(self):
        return os.urandom(16)


    def _generate_client_secret(self):
        in_t = 'NAi7hGHZtDY0'
        pre = ":"
        post = "@"
        plaintext = f"{randint(10, 99)}{pre}{in_t}{post}{randint(10, 99)}"
        pval = 16 - (len(plaintext) % 16)
        ptext = plaintext.encode('utf-8') + bytes([pval] * pval)
        iv = self._generate_iv()
        cipher = AES.new(self.key.encode('utf-8'), AES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(pad(ptext, 16))
        encrypted_data = hexlify(iv + ciphertext).decode('utf-8')
        return encrypted_data

    def _make_curl_request(self, method, url, headers=None, data=None):
        curl_command = f"""curl -X {method} "{url}" """
        if headers:
            curl_command += ''.join([f""" -H "{key}: {value}" """ for key, value in headers.items()])
        if data:
            curl_command += f""" -d "{data}" """
        print(curl_command)
        curl_process = subprocess.Popen(curl_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        curl_output, curl_error = curl_process.communicate()
        try:
            return json.loads(curl_output)
        except json.JSONDecodeError as e:
            print("Error with curl", e)
            return None

    def first_call(self):
        url = f"{self.base_url}account/authorize"
        state = self._generate_random_number()
        param = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'state': state
        }
        print("firstcall***************")
        print(param)
        x = [f"""{key}={value}""" for key, value in param.items()]
        redirect_url = f"""{url}?{'&'.join(x)}"""
        return redirect_url

    def _second_call(self, code):
        url = f"{self.base_url}account/token"
        secret_key = self._generate_client_secret()
        params = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.redirect_uri,
            'client_id': self.client_id,
            'client_secret': secret_key
        }
        print("_second_call******************")
        data = '&'.join([f"{key}={value}" for key, value in params.items()])
        return self._make_curl_request("POST", url, headers={'Content-Type': 'application/x-www-form-urlencoded'}, data=data)

    def second_call(self, code):
        res = self._second_call(code=code) 
        print("second_call******************")
        print(res)
        if "access_token" in res:
            access_token = res["access_token"]
            url = f"{self.base_url}account/resource"
            headers = {'Authorization': f'Bearer {access_token}'}
            return self._make_curl_request("GET", url, headers=headers)
        else:
            return "No Access Token"
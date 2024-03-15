import subprocess
import json
import random, os
from random import randint
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from binascii import hexlify
import base64
import datetime
import socket
import subprocess
import requests
from mainapp.Encrypt import DataEncryption

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
        # print(curl_command)
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
        # print("firstcall***************")
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
        # print("_second_call******************")
        data = '&'.join([f"{key}={value}" for key, value in params.items()])
        return self._make_curl_request("POST", url, headers={'Content-Type': 'application/x-www-form-urlencoded'}, data=data)

    def second_call(self, code):
        res = self._second_call(code=code)
        # print("second_call******************")
        print(res)
        if "access_token" in res:
            access_token = res["access_token"]
            url = f"{self.base_url}account/resource"
            headers = {'Authorization': f'Bearer {access_token}'}
            return (self._make_curl_request("GET", url, headers=headers),{'access_token':access_token})
        else:
            return "No Access Token"


class ProfileApi:
    def __init__(self):
        # key = base64.b64decode(os.getenv('pkey').encode('utf-8'))
        key = base64.b64decode('c+cNh7y44v4wLjb30U2xwcbimGz0ci4VoSxmQvhC94o=')
        self.key = key
        self.clientId='P004'
        self.url='https://bridgeuat.csccloud.in/profile/vle/info'

    def get_client_ip(self):
        ip = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ip.connect(("8.8.8.8", 80))
        return ip.getsockname()[0]

    def generate_transaction_id(self):
        return "".join(["{}".format(random.randint(0, 9)) for _ in range(0, 27)])

    def create_request_data(self, csc_id, txn, ts):
        return f"csc_id={csc_id}|vle_type=V|txn={txn}|ts={ts}"

    def profile_api_request(self, req_data):
        client_ip = self.get_client_ip()
        obj= DataEncryption(self.key)
        enc_data=obj.encryptFun(req_data)
        final_data = {
            "client_id": self.clientId,
            "client_ip": client_ip,
            "req_data": enc_data.decode('utf-8'),
        }
        print("final data",final_data)
        # http = urllib3.PoolManager()
        # headers = {'Content-Type': 'application/json'}
        # response = http.request('POST', url=self.url, body=json.dumps(final_data), headers=headers)
        response=subprocess.run(["curl", "-X", "POST", "-H", f'Content-Type: application/json', "-d", f'{json.dumps(final_data)}', self.url], capture_output=True)
        print('response=',response,type(response))
        if response.stdout is not None:
            jdata = json.loads(response.stdout)
            # print('profile api reps=',jdata,'\n\n')
            return jdata
        else:
            return {"error": "No response from subprocess"}

    def filter_data_fun(self, res_data):
        data_items = res_data.split('|')
        data_dict = {}
        for item in data_items:
            parts = item.split('=')
            key = parts[0]
            value = "=".join(parts[1:])
            data_dict[key] = value
        # return (data_dict.get('mobile'), data_dict.get('email'), data_dict.get('geo_long'), data_dict.get('geo_lat'), data_dict.get('gender'), data_dict.get('dob'), data_dict.get('loc_type'), data_dict.get('district'), data_dict.get('state'), data_dict.get
        # ('postal_code'))
        return data_dict

    def main(self, csc_id):
        ts = datetime.datetime.now().replace(microsecond=0, second=0).isoformat()
        txn = self.generate_transaction_id()
        req_data = self.create_request_data(csc_id, txn, ts)
        response_data = self.profile_api_request(req_data)
        print(response_data)
        if response_data['res_data'] != "NA":
            # try:
                dec_data = response_data['res_data']
                # print("dec_data",dec_data,"\n\n")
                obj= DataEncryption(self.key)
                decp_data=obj.decrptFun(dec_data,1)
                print("decp_data=",decp_data)
                response = self.filter_data_fun(decp_data)
                return response
            # except Exception as e:
            #     return str(e) + ' ' + csc_id
        else:
            return None


def generate_otp_function():
    random_number = random.randint(100000, 999999)
    return random_number

def new_mssg_api(mobileNo,otp):
    url = "https://pgapi.vispl.in/fe/api/v1/send"
    param={"username":"cscotppg1.trans",
           "password":"SU69z",
           "unicode":"false",
           "from":"CSCSPV",
           "to":mobileNo,
           "dltPrincipalEntityId":"1301157363501533886",
           "dltContentId":"1707170929719904959",
           "text":f"Your verification code for Digipay(CSC) login is: {otp}"
    }

    payload = {}
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Token 8cd6fcaab8d3d043335f3b9d19d98c9905348447'
    }

    response = requests.request("POST", url, headers=headers, data=payload,params=param)

    # print("sms resp text",response.text)
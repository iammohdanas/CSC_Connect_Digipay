import datetime
import json
import requests
from mainapp.Encrypt import aes_decrypt, aes_encrypt


def micro_service_config(req_action_data):
    # Encrypt request data
    req_dat = {
        'clientId': req_action_data['clientId'],
        'reqData': aes_encrypt(req_action_data['payLoad'], req_action_data['clientToken'])
    }
    payload = json.dumps(req_dat)
    print("payload *************",payload)
    # Request caller
    res = micro_caller(req_action_data['apiUrl'], payload, req_action_data['apiTimeout'])
    print("res ************")
    print(res)
    if res['resCode'] == '000':
        dcp = aes_decrypt(res['resData'], req_action_data['clientToken'])
        if dcp:
            return dcp['body']
        else:
            return False
    else:
        return False

def micro_caller(url, payload, api_timeout):
    headers = {'Content-Type': 'application/json'}
    print("\n headers", headers)
    print("\n url ******",url)
    print("\n ***** API Timeout",)
    try:
        response = requests.post(url, data=payload, headers=headers, timeout=api_timeout, verify=False)
        print("**************",response)
        response_json = response.json()
        csr = {
            'resCode': response_json.get('resCode', '003'),
            'resMsg': response_json.get('resMsg'),
            'resData': response_json.get('resData')
        }
    except requests.RequestException as e:
        csr = {
            'resCode': '003',
            'resMsg': str(e),
            'resData': None
        }
    return csr









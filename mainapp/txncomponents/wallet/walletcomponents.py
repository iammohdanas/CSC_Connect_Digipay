import datetime
import json
from xml.etree.ElementTree import XMLParser

import requests
from mainapp.Encrypt import aes_decrypt, aes_encrypt

from mainapp.components import get_client_ip_address
from mainapp.configdata.appconfig import API_VERBOSE, APPNAME, WAL_CLIENT, WAL_CREDIT, WAL_DEBIT, WAL_MINBALANCE, WAL_TIMEOUT, WAL_TOKEN, WAL_URL



def wallet_request(bd, req_action):
    # wallet configuration parameters
    r = {
        'walClient': WAL_CLIENT,
        'walToken': WAL_TOKEN,
        'walTimeout': WAL_TIMEOUT,
        'apiVerbose': API_VERBOSE
    }
    
    if req_action.upper() == 'DEBIT':
        r['walActionUri'] = WAL_URL + WAL_DEBIT
    elif req_action.upper() == 'CREDIT':
        r['walActionUri'] = WAL_URL + WAL_CREDIT
    
    # request header
    r['inp'] = {
        'head': {
            'clientId': r['walClient'],
            'appName': APPNAME,
            'refId': bd['deviceTxn'],
            'ts': datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
            'reqAction': 'credit',
            'clientIp': get_client_ip_address()
        },
        # request body
        'body': {
            'cscId': bd['ownerId'],
            'ownerId': bd['ownerId'],
            'dataSet': 'dgp',
            'isoRrn': bd['custRef'],
            'txnAmount': bd['walletAmount'],
            'remarks': bd['acquirerId'] + '- CUS:' + bd['custId'][-4:],
            'refTxn': bd['authorizeCode'] if 'authorizeCode' in bd else bd['deviceTxn'],
            'txnSource': bd['txnType'],
            'reqCode': bd['reqCode'],
            'txnDate': datetime.now().strftime('%Y-%m-%d'),
            'minBalance': bd['minBalance'] if 'minBalance' in bd else WAL_MINBALANCE
        }
    }
    
    return r


def wallet_req_action(bd):
    r = {
        'apiUrl': bd['walActionUri'],
        'clientId': bd['walClient'],
        'clientToken': bd['walToken'],
        'apiTimeout': bd['walTimeout'],
        'apiVerbose': bd['apiVerbose'],
        'payLoad': bd['inp']
    }
    
    return micro_service_config(r)['resp']


def fetch_bal_amt(amt):
    bal = 'NA'
    if amt:
        bal_arr = amt.split('C')
        if len(bal_arr) > 1:
            bal = int(bal_arr[1])
    return bal


def micro_caller(url, payload, api_timeout):
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(url, data=payload, headers=headers, timeout=api_timeout, verify=False)
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


def micro_service_config(r):
    # Encrypt request data
    req_dat = {
        'clientId': r['clientId'],
        'reqData': aes_encrypt(r['payLoad'], r['clientToken'])
    }
    payload = json.dumps(req_dat)
    # Request caller
    res = micro_caller(r['apiUrl'], payload, r['apiTimeout'])
    if res['resCode'] == '000':
        dcp = aes_decrypt(res['resData'], r['clientToken'])
        if dcp:
            return dcp['body']
        else:
            return False
    else:
        return False





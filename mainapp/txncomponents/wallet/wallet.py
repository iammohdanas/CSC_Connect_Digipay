from datetime import datetime
import json
from mainapp.components import get_client_ip_address
from mainapp.configdata.appconfig import AEPS, API_VERBOSE, APPNAME, IBLDMT, WAL_CLIENT, WAL_CREDIT, WAL_DEBIT, WAL_MINBALANCE, WAL_TIMEOUT, WAL_TOKEN, WAL_URL, ACQUIRERID
from mainapp.txncomponents.wallet.walletUtils import micro_service_config

def wallet_request(configinputwallet, req_action):
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
            'refId': 'deviceTxn',
            'ts': datetime.now().strftime('%Y-%m-%dT%H:%M:%S'),
            'reqAction': 'CREDIT',
            'clientIp': 'get_client_ip_address()'
        },
        # request body
        'body': {
            'cscId': configinputwallet['cscId'],
            'ownerId': configinputwallet['ownerId'],
            'dataSet': 'dgp',
            'isoRrn': "configinputwallet['custRef']",
            'txnAmount': configinputwallet['txnAmount'],
            'remarks': ACQUIRERID + '- CUS:' + IBLDMT['CUSTOMER_ID'][-4:],
            'refTxn': "configinputwallet['authorizeCode']" if 'authorizeCode' in configinputwallet else "configinputwallet['deviceTxn']",
            'txnSource': AEPS['CW_TXNTYPE'],
            'reqCode': AEPS['CW_REQCODE'],
            'txnDate': datetime.now().strftime('%Y-%m-%d'),
            'minBalance': "configinputwallet['minBalance']" if 'minBalance' in configinputwallet else WAL_MINBALANCE
        }
    }
    return r

def wallet_req_action(wallet_req_data):
    print("n\nwallet_req_data",wallet_req_data)
    req_action_data = {
        'apiUrl': wallet_req_data['walActionUri'],
        'clientId': wallet_req_data['walClient'],
        'clientToken': wallet_req_data['walToken'],
        'apiTimeout': wallet_req_data['walTimeout'],
        'apiVerbose': wallet_req_data['apiVerbose'],
        'payLoad': wallet_req_data['inp']
    }
    return micro_service_config(req_action_data)['resp']


from audioop import reverse
import base64
import datetime
from datetime import datetime
import time
from functools import wraps
from io import BytesIO
import json
from pyexpat import XMLParserType
from xml.etree.ElementTree import XMLParser
from django.shortcuts import redirect, render
import requests
import xmltodict
from mainapp.components import bank_list, generate_msg_id, generate_txn_id, get_client_ip_address
from mainapp.configdata.appconfig import ACQUIRERID, AEPS_VER, SWITCH_TYPE
from mainapp.models import DeviceAuth, DeviceFetch,DeviceRegister
from mainapp.txncomponents.IBLPayout.IBLPayout import process_IBL_txn
from mainapp.txncomponents.wallet.wallet import wallet_req_action, wallet_request
from mainapp.txncomponents.wallet.walletcomponents import fetch_bal_amt
from mainapp.txncomponents.withdrawformreq import RespPay, withdraw_apireq
from .connect import Connect, ProfileApi, generate_otp_function, new_mssg_api
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from .connect import Connect
import matplotlib.pyplot as plt
import numpy as np
from django.contrib.auth import logout
from datetime import datetime, timedelta
import mysql.connector
from xml.parsers.expat import ExpatError
# Assuming connector is a custom class in your Django app

client_id = "e0065bb4-b648-419b-e973-2e6e49552bd7"
redirect_uri = "http://localhost:9000/digipay-npci-connect-login/"
client_key = 's2gISpnceiVIWxbB'
connector = Connect(client_id, redirect_uri, client_key)


def login(request):
    if request.session.get("access_token") is not None:
        return render(request, 'dashboard.html')
    else:
        return render(request, 'login.html')

def redirect_fun(request):
    return redirect(connector.first_call())

def process_login(request):
    if request.method == 'POST':
        # access_token=''
        print("in post method")
        otp = int(request.POST.get('otp'))
        # print("otp",otp,"type",type(otp))
        # print("otp_session",request.session.get('otp'),"type",type(request.session.get('otp')))
        if otp == request.session.get('otp'):
            # OTP is valid
            
            context = {
                'otp_verified': True,
                'otp_verify_message': "OTP verification successful!",
            }
            # return redirect('index.html')
        else:
            # OTP is invalid
            context = {
                'otp_verified': False,
                'otp_verify_message': "Invalid OTP. Please try again.",
            }
        # print("context",context)
        request.session['context_data']=context
        
        # return redirect('welcome')  
        return render(request, 'authentication/login_verify.html',context)
    elif request.method=="GET":
        print("in get method")
        if request.GET.get('code'):
            code = request.GET.get('code')
            if not request.session.get("second_call_data"):
                print("in if")
                data = connector.second_call(code=code)
                print(data)
                # access_token=data

                # print("access token",access_token)
                # request.session["connect_data0"]=data[1]["access_token"]
                request.session["second_call_data"]=data
                request.session["access_token"] = data[1]
            else:
                print("in else")
                data=request.session.get("second_call_data")
                print("second_call_data",data)
                access_token = request.session.get("access_token")
                print("*********",access_token)
                # request.session["access_token0"]=data
            # print("access token",access_token)
            print("data",data)
            
            csc_id = data[0]['User']['csc_id']
            request.session['cscid'] = csc_id
            request.session['owner'] = data[0]['User']['owner']
            obj = ProfileApi()
            user_data = obj.main(csc_id)
            vle_name =user_data.get('vle_name')
            request.session['vle_name']=vle_name
            vle_name=request.session.get('vle_name')
            agent_id=user_data.get('agent_id')
            request.session['agent_id']=agent_id
            terminal_id=user_data.get('terminal_id')
            request.session['terminal_id']=terminal_id
            mobile_no = user_data['mobile']
            otp = generate_otp_function()   
            new_mssg_api("8858045785", otp)
            request.session['otp'] = otp
            request.session['mobile'] = mobile_no
            context = {
                'otp_generated': True,
                    'otp_sent_message': f"OTP sent to {mobile_no}.",
                }
            # return redirect("login_verify.html")
            context = {
                'otp_generated': False,
                'otp_sent_message': 'error..!',
            }
            return render(request, 'authentication/login_verify.html', context)
    return render(request, 'authentication/login_verify.html')


def verify_otp(request):
    if request.method == 'POST':
        otp = int(request.POST.get('otp'))
        print("otp",otp,"type",type(otp))
        print("otp_session",request.session.get('otp'),"type",type(request.session.get('otp')))
        if otp == request.session.get('otp'):
            context = {
                'otp_verified': True,
                'otp_verify_message': "OTP verification successful!",
            }
            request.session['otpverifystatus'] = context
            return redirect('dashboarddigipay')  
        else:
            context = {
                'otp_verified': False,
                'otp_verify_message': "Invalid OTP. Please try again.",
            }
            return render(request, 'authentication/login_verify.html',context) 
        print("context",context)
    request.session['context_data']=context
    return HttpResponse("Error 404")

def afterloginbioauth(request):
    if request.session.get('otpverifystatus')==True:
        return redirect('dashboarddigipay')
    else:
        return redirect('authdevregister') 

def access_token_required(next_func):
    @wraps(next_func)
    def wrapper(request):
        if request.session.get("access_token") is not None:
            return next_func(request)
        else:
            return render(request, 'login.html')
    return wrapper

@access_token_required
def transactionform(request):
    aeps_service = ["Withdraw: Allows users to withdraw cash from their bank account using their Aadhaar number and fingerprint authentication.",
                      "Deposit: Enables users to deposit cash into their bank account using Aadhaar authentication.", 
                      "Mini statement: Provides a brief overview of recent transactions and account balance.",
                      "Fund transfer: Facilitates the transfer of funds between bank accounts linked with Aadhaar authentication."]
    device_exists = DeviceFetch.objects.exists()
    context = {
                'bank_data':bank_list(),
                'aeps_service': aeps_service,
                'device_exists':device_exists
            }
    return render(request, 'transaction/transactionform.html', context)

@access_token_required
def process_withdrawform(request):
    configinput = {}
    configinput2 ={}
    if request.method == 'POST':
        configinput["customer_mobile_number"] = request.POST.get('customermobilenumber')
        configinput["aadhar_number"] = request.POST.get('aadharNumber')
        configinput["txn_amount"] = request.POST.get('amount')
        configinput["bank_shortcode"] = request.POST.get('bankOption')
        configinput["transaction_type"] = request.POST.get('transactionType', None)
        pidOptions = request.POST.get('Pid_Options')
        pidData = request.POST.get('Pid_Data')
        print('*********Pid Data',pidData)
        print('****Pid Option',pidOptions)
        device_info = request.POST.get('device_info')
        print("deviceInfoFingerprint******************")
    
    device_info = xmltodict.parse(device_info)
    configinput["dpId"] = device_info['DeviceInfo']['@dpId']
    configinput["dc"] = device_info['DeviceInfo']['@dc']
    configinput["rdsId"] = device_info['DeviceInfo']['@rdsId']
    configinput["rdsVer"] = device_info['DeviceInfo']['@rdsVer']
    configinput["mi"] = device_info['DeviceInfo']['@mi']
    configinput["mc"] = device_info['DeviceInfo']['@mc']

    if pidData:
        pidData = xmltodict.parse(pidData)
        configinput["ci_value"] = pidData['PidData']['Skey']['@ci']
        configinput["Skey_Value"] = pidData['PidData']['Skey']['#text']
        configinput["Hmac_Value"] = pidData['PidData']['Hmac']
        configinput["dataValue"] = pidData['PidData']['Data']['#text']
    else:
        pidData = None

    txn_id = generate_txn_id(request)   
    msg_id = generate_msg_id(request)
    configinput2["txnId"] = txn_id
    request.session['txn_id'] = configinput2["txnId"]
    configinput2["msgId"] = msg_id
    configinput2["callbackEndpointIP"] = "127.0.0.1"
    request.session['aadhar_number'] = configinput["aadhar_number"]
    print("aadhar_number",request.session.get('aadhar_number'))
    request.session['txn_amount']= configinput["txn_amount"]
    current_local_time = datetime.now()
    offset_seconds = -time.timezone if (time.localtime().tm_isdst == 0) else -time.altzone
    offset_hours = offset_seconds // 3600
    offset_minutes = (offset_seconds % 3600) // 60
    offset_str = "{:02d}:{:02d}".format(abs(offset_hours), abs(offset_minutes))
    offset_str = ("+" if offset_hours >= 0 else "-") + offset_str
    configinput2["ts"] = current_local_time.strftime('%Y-%m-%dT%H:%M:%S') + offset_str
    request.session['ts'] = configinput2["ts"]
   

    api_req_data_context = withdraw_apireq(configinput, configinput2)
    context = {
        **api_req_data_context,
    }
    xml_data = xmltodict.unparse({"xml": context}, full_document=False)
    xml_data = xml_data.replace('<ns2ReqPay', '<ns2:ReqPay').replace('</ns2ReqPay>', '</ns2:ReqPay>')
    xml_data = xml_data.replace('xmlnsns2="http://npci.org/upi/schema/"', 'xmlns:ns2="http://npci.org/upi/schema/"')
    xml_data = xml_data.replace('xmlnsns3="http://npci.org/cm/schema/"','xmlns:ns3="http://npci.org/cm/schema/"')
    xml_response = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n' + xml_data
    return HttpResponse(xml_response, content_type="application/xml")


def authdevregister(request):
    auth_reg_instructions = ["Click on Scan New Devices",
                            "The Device will be fetched and displayed", 
                            "Once the Device gets diplayed, Enter your purpose for new device registration",
                            "Click Register button to register new device."]
    device_exists = DeviceFetch.objects.exists()
    context = {
        'auth_reg_instructions' : auth_reg_instructions, 'device_exists':device_exists
    }
    return render(request, 'transaction/authregister.html',context)

@access_token_required
def passbook(request):
    device_exists = DeviceFetch.objects.exists()
    #DB fetch start
    conn = mysql.connector.connect(host='127.0.0.1', password = 'AATricks372!', user= 'root')
    db_cursor = conn.cursor()
    db_cursor.execute("USE npci")
    # Execute a SELECT query to retrieve data from the npci_resp_table
    db_cursor.execute("SELECT * FROM npci_resp_table")
    # print('database created')
    rows = db_cursor.fetchall()
    i = 1
    # Process the retrieved data
    data_passbook = []
    for row in rows:
        user_txndata = {}
        xml_data = row[2]
        try:
            json_data = xmltodict.parse(xml_data)
            json_data_dump = json.dumps(json_data)
            json_data_loads = json.loads(json_data_dump)
            # print(json_data_loads)
            if 'ns2:RespPay' in json_data_loads:
                cust_ref = json_data_loads['ns2:RespPay']['Txn']['@custRef']
                ts = json_data_loads['ns2:RespPay']['Txn']['@ts']
                dt_object = datetime.fromisoformat(ts)
                # Convert datetime object to desired format
                normal_date_time = dt_object.strftime('%Y-%m-%d %H:%M:%S')
                org_amount = json_data_loads['ns2:RespPay']['Resp']['Ref'][0]['@orgAmount']
                purpose = json_data_loads['ns2:RespPay']['Txn']['@purpose']
                if purpose == '22':
                    purpose = 'Dr'
                elif purpose == '23':
                    purpose = 'Cr'
                # print(i," CustRef respay:", cust_ref)
                # print(ts)
                # print('org amount', org_amount)
                # print("purpose:", purpose)
                user_txndata= {
                    's_no.': i,
                    'db_s_no':row[0],
                    'cust_ref':cust_ref,
                    'ts':normal_date_time,
                    'org_amount':org_amount,
                    'purpose':purpose
                }
                data_passbook.append(user_txndata)
                i = i+1
                
            elif 'ns2:Ack' in json_data_loads:
                ack_data = json_data_loads
        except ExpatError as e:
            print(f"Error parsing XML data: {e}")
    return render(request, 'transaction/passbook.html', {'device_exists':device_exists,'data_passbook': data_passbook})

@access_token_required
def aepspassbook(request):
    return render(request,'transaction/aepspassbook.html')

@access_token_required
def aepslogs(request):
    device_exists = DeviceFetch.objects.exists()
    return render(request,'transaction/aepslogs.html',{'device_exists':device_exists})

@access_token_required
def dashboard(request):
    vle_name=request.session.get('vle_name')
    csc_id = request.session.get('cscid')
    context = {'vle_name':vle_name, 'csc_id':csc_id}
    return render(request,'dashboard.html',context)

@access_token_required
def dashboardcsc(request):
    vle_name=request.session.get('vle_name')
    csc_id = request.session.get('cscid')
    context = {'vle_name':vle_name, 'csc_id':csc_id}
    return render(request,'dashboardcsc.html',context)

@access_token_required
def dashboarddigipay(request):
    vle_name=request.session.get('vle_name')
    csc_id = request.session.get('cscid')
    current_month = datetime.now().strftime("%B")
    device_exists = DeviceFetch.objects.exists()
    context = {'vle_name':vle_name, 'csc_id':csc_id, 'current_month':current_month,'device_exists':device_exists}
    return render(request,'dashboarddigipay.html',context)

def base2(request):
    vle_name=request.session.get('vle_name')
    csc_id = request.session.get('cscid')
    device_exists = DeviceFetch.objects.exists()
    context = {'vle_name':vle_name, 'csc_id':csc_id, 'device_exists':device_exists}
    return render(request,'base2.html',context)

def baseauth(request):
    vle_name=request.session.get('vle_name')
    csc_id = request.session.get('cscid')
    context = {'vle_name':vle_name, 'csc_id':csc_id}
    return render(request,'baseauth.html',context)

def bioauthlogin(request):
    device_exists = DeviceFetch.objects.exists()
    return render(request,'authentication/bioauthlogin.html',{'device_exists':device_exists})

@access_token_required
def payout(request):
    csc_id = request.session.get('cscid')
    return render(request,'transaction/payout.html',{'csc_id':csc_id})

@access_token_required
def aepstransaction(request):
    vle_name=request.session.get('vle_name')
    csc_id = request.session.get('cscid')
    
    context = {'vle_name':vle_name, 'csc_id':csc_id}
    return render(request,'aepstransaction.html',context)

def res_acquirer_ack(request):
    dat={'ipAddr': get_client_ip_address(),
         'acquirerId':ACQUIRERID,
         'switchType':SWITCH_TYPE,
         'msgType': 'ALIVE',
         'ver':AEPS_VER,       
         }
    rs = ''
    if rs.get('curlHttp') == '200' and rs.get('curlErr') == 0 and rs.get('curlRes'):
        rx = XMLParserType.decode(rs.get('curlRes', ''))
    else:
        rx = {
        }
    res = {
        'refId': dat['refId'],
        'acquirerId': dat['acquirerId'],
        'switchType': dat['switchType'],
        'msgType': dat['msgType'],
        'ver': dat['ver'],
        'api': rx.get('ns2:Ack_attr', {}).get('api') if rx else None,
        'reqMsgId': rx.get('ns2:Ack_attr', {}).get('reqMsgId') if rx else None,
        'ackTs': rx.get('ns2:Ack_attr', {}).get('ts') if rx else None,
        'curlErr': rx.get('curlErr') if rx else None,
        'errCode': rx.get('ns2:Ack', {}).get('errorMessages', {}).get('errorCd') if rx else None,
        'errMsg': rx.get('ns2:Ack', {}).get('errorMessages', {}).get('errorDtl') if rx else None,
        'ipAddr': dat['ipAddr']
    }
    if res['errCode'] is None:
        res_code = '000'
        res['txnStatus'] = 'SUCCESS'
    else:
        res_code = '003'
        res['txnStatus'] = 'FAILED'
        if len(res['errCode']) > 15:
            res['errCode'] = 'UW'
    
    api_resp_data_context = RespPay(res)
    context = {
        **api_resp_data_context,
    }
    xml_data = xmltodict.unparse({"xml": context}, full_document=False)
    return HttpResponse(xml_data, content_type="application/xml")

@access_token_required
def walletTopup(request):
    with open('mainapp/data/transaction/wallet_topup.json', 'r') as json_file:
        data = json.load(json_file)
    device_exists = DeviceFetch.objects.exists()
    return render(request,'transaction/walletTopup.html',{'instruction_data': data,'device_exists':device_exists} )

@access_token_required
def wallet_topup_process(request):
    configinputwallet = {}
    configinputwallet['txnAmount'] = request.POST.get('wallettopupinputamount')
    # configinputwallet['inp']['body']['txnAmount'] = request.POST.get('wallettopupinputamount')
    configinputwallet['cscId'] = request.session.get("cscId")
    configinputwallet['ownerId'] = request.session.get("owner")
    # Create wallet request
    wallet_req_data = wallet_request(configinputwallet, req_action='CREDIT') 
    # Perform wallet action
    response_data = wallet_req_action(wallet_req_data)
    # Prepare JSON response
    response = {
        'response_data': response_data
    }
    print(response)
    return JsonResponse(response)


# def initiate_payment(request):
    
#     data = process_IBL_txn()
#     process_txn_api_url = 'https://indusapiuat.indusind.com/indusapi-np/uat/sync-apis/ISync/ProcessTxn'
#     response = requests.post(process_txn_api_url, json=data)
    
#     return JsonResponse(response.json())

def logout_user(request):
    if request.method == 'GET':
        
        logout(request)
        return render(request, 'login.html', {'logged_out': True})
    else:
        return HttpResponse('Invalid request method', status=404)
    
# def saveauthdb(request):
#     # data = json.loads(request.body)
#     csc_id = request.session.get('csc_Id')
#     # mac_address = data.get('mac_address')
#     # ports = data['dev_infos']['ports']
#     # ports_int = [int(port) for port in ports]
#     csc_Id=csc_id,
#     port=8080,
#     status='okay',
#     info='Ready',
#     mi='dummy mi',
#     dc='dummy dc',
#     mac='dummy mac_address',
#     purpose='testing2'
#     device_exists = DeviceFetch.objects.exists()
#     device, created = DeviceFetch.objects.get_or_create(
#             id=1,  # Assuming there is only one entry in the table, so we use a fixed id
#             defaults={
#                 'port': port,
#                 'status': status,
#                 'info': info,
#                 'dc': dc,
#                 'mi': mi,
#                 'mac': mac,
#                 'csc_Id': csc_id,
#                 'purpose': purpose
#             }
#         )

#         # If the entry already existed, update its values with the new ones
#     if not created:
#         device.port = port
#         device.status = status
#         device.info = info
#         device.dc = dc
#         device.mi = mi
#         device.mac = mac
#         device.csc_Id = csc_id
#         device.purpose = purpose
#         device.save()
#         return HttpResponse('updated {0}'.format(device_exists), status = 200)
#     return HttpResponse('created', status = 200)

@access_token_required
def mini_statement(request):
    vle_name=request.session.get('vle_name')
    csc_id = request.session.get('cscid')
    context = {'vle_name':vle_name, 'csc_id':csc_id}
    return render(request,'transaction/ministatement.html',context)

@access_token_required
def base_receipt(request):
    # import pdb;  pdb.set_trace()
    context = {'vle_name':request.session.get('vle_name'),
               'csc_id': request.session.get('cscid'),
               'agent_id':request.session.get('agent_id'),
               'terminal_id':request.session.get('terminal_id'),
               'aadhar_number':"X"*(8) + (request.session.get('aadhar_number'))[8:] ,
               'date_ts': request.session.get('ts'),
               'txn_id': request.session.get('txn_id'),
               'txn_amount': request.session.get('txn_amount'),
               }
    return render(request,'base_receipt.html',context)
    
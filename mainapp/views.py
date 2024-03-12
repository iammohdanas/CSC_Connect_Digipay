from audioop import reverse
from functools import wraps
import json
from pyexpat import XMLParserType
from django.shortcuts import redirect, render
import xmltodict
from mainapp.components import bank_list, generate_msg_id, generate_txn_id
from mainapp.models import DeviceAuth,DeviceRegister
from mainapp.txncomponents.withdrawformreq import RespPay, withdraw_apireq
from .connect import Connect, ProfileApi, generate_otp_function, new_mssg_api
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from .connect import Connect
# Assuming connector is a custom class in your Django app

client_id = "e0065bb4-b648-419b-e973-2e6e49552bd7"
redirect_uri = "http://localhost:9000/digipay-npci-connect-login/"
client_key = 's2gISpnceiVIWxbB'
connector = Connect(client_id, redirect_uri, client_key)

def login(request):
    return render(request, 'login.html')

def redirect_fun(request):
    return redirect(connector.first_call())

# def process_login(request):
#     code = request.GET.get('code')
#     if not code:
#         return redirect('login')
#     data = connector.second_call(code=code)
#     # print(data)
#     print("data", data)
#     print("access_token" ,data[1])
#     csc_id = data[0]['User']['csc_id']
#     obj = ProfileApi()
#     user_data = obj.main(csc_id)
#     mobile_no = user_data['mobile']
#     otp = generate_otp_function()   
#     new_mssg_api("8858045785", otp)
#     request.session['otp'] = otp
#     request.session['mobile'] = mobile_no
#     context = {'bank_data':bank_list()}
#     if isinstance(data, dict):
#         return render(request, 'authentication/login_verify.html',context)
#     else:
#         return JsonResponse({"error": "Invalid data format"}, status=400)

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
            obj = ProfileApi()
            user_data = obj.main(csc_id)
            mobile_no = user_data['mobile']
            otp = generate_otp_function()   
            new_mssg_api("7017528755", otp)
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
            return redirect('transactionform')  
        else:
            context = {
                'otp_verified': False,
                'otp_verify_message': "Invalid OTP. Please try again.",
            }
            return render(request, 'authentication/login_verify.html',context) 
        print("context",context)
    request.session['context_data']=context
        
    return HttpResponse("Error 404")

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
    context = {
                'bank_data':bank_list(),
                'aeps_service': aeps_service,
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
        pidOptions = request.POST.get('pid_options')
        pidData = request.POST.get('pid_data')
        device_info = request.POST.get('device_info')
        print("deviceInfoFingerprint******************")

    device_info = xmltodict.parse(device_info)
    configinput["dpId"] = device_info['DeviceInfo']['@dpId']
    configinput["dc"] = device_info['DeviceInfo']['@dc']
    configinput["rdsId"] = device_info['DeviceInfo']['@rdsId']
    configinput["rdsVer"] = device_info['DeviceInfo']['@rdsVer']
    configinput["mi"] = device_info['DeviceInfo']['@mi']
    configinput["mc"] = device_info['DeviceInfo']['@mc']

    pidData = xmltodict.parse(pidData)
    configinput["ci_value"] = pidData['PidData']['Skey']['@ci']
    configinput["Skey_Value"] = pidData['PidData']['Skey']['#text']
    configinput["Hmac_Value"] = pidData['PidData']['Hmac']
    configinput["dataValue"] = pidData['PidData']['Data']['#text']

    txn_id = generate_txn_id(request)   
    msg_id = generate_msg_id(request)
    configinput2["txnId"] = txn_id
    configinput2["msgId"] = msg_id
    configinput2["callbackEndpointIP"] = "127.0.0.1"

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
    DeviceRegister.objects.create(
                device_name=request.POST.get('device_name'),
                purpose=request.POST.get('input_purpose')
            )
    return render(request, 'transaction/authregister.html')

@access_token_required
def walletTopup(request):
    with open('mainapp/data/transaction/wallet_topup.json', 'r') as json_file:
        data = json.load(json_file)
    return render(request,'transaction/walletTopup.html',{'instruction_data': data} )

def res_acquirer_ack(request):
    dat={'ipAddr':'',
         'acquirerId':'',
         'switchType':'',
         'msgType': '',
         'ver':'',
         'ipAddr': '127.0.0.1'        
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
        'api': rx.get('ns2:Ack_attr', {}).get('api'),
        'reqMsgId': rx.get('ns2:Ack_attr', {}).get('reqMsgId'),
        'ackTs': rx.get('ns2:Ack_attr', {}).get('ts'),
        'curlErr': rx.get('curlErr'),
        'errCode': rx.get('ns2:Ack', {}).get('errorMessages', {}).get('errorCd'),
        'errMsg': rx.get('ns2:Ack', {}).get('errorMessages', {}).get('errorDtl'),
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





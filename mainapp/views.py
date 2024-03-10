from audioop import reverse
from functools import wraps
from django.shortcuts import redirect, render
import xmltodict
from mainapp.components import bank_list, generate_msg_id, generate_txn_id
from mainapp.models import DeviceAuth
from mainapp.txncomponents.withdrawformreq import withdraw_apireq
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
                'bank_data':bank_list(),
                'otp_verified': True,
                'otp_verify_message': "OTP verification successful!",
            }
            return render(request, 'transaction/transactionform.html',context)  
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

def save_to_database(request):
    if request.method == 'POST':
        data = request.POST  # Assuming your JavaScript sends data as POST request
        csc_id = request.POST.get('csc_id')
        port_number = request.POST.get('port')
        hmac = request.POST.get('hmac')
        device_id = request.POST.get('device_id')
        port_exists = DeviceAuth.objects.filter(port=port_number).exists()
        if not port_exists:
            # saving data to database
            DeviceAuth.objects.create(
                csc_id=data.get('httpStatus', False),
                device_id=data.get('data', ''),
                port=port_number,
                hmac=data.get('status', ''),
            )
            return JsonResponse({'message': 'Data saved successfully'})
        else:
            return JsonResponse({'port_number': port_number}, status=400)
        # Optionally, you can return a JsonResponse to your JavaScript frontend
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
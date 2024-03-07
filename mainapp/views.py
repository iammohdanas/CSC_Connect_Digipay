from audioop import reverse
from functools import wraps
from django.shortcuts import redirect, render
import xmltodict
from mainapp.components import bank_list, generate_msg_id, generate_txn_id
from mainapp.txncomponents.withdrawformreq import withdraw_apireq
from .connect import Connect
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

def process_login(request):
    code = request.GET.get('code')
    if not code:
        return redirect('login')
    data = connector.second_call(code=code)
    context = {'bank_data':bank_list()}
    if isinstance(data, dict):
        return render(request, 'transaction/transactionform.html',context)
    else:
        return JsonResponse({"error": "Invalid data format"}, status=400)

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


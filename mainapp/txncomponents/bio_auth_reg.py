import json
from django.http import JsonResponse

from mainapp.models import DeviceFetch


def registered_device_api(request):
    try:
        if request.method=="POST":
            # Assuming the request body contains the ports array
            data = json.loads(request.body)
            print("data return",data)
            csc_id = request.session.get('csc_Id')
            print("csc_id",csc_id)
            # mac_address = data.get('mac_address')
            mac_address=2249190931
            print("mac_address return",mac_address)
            
            # Filter devices based on csc_id and mac address
            # registered_devices = DeviceFetch.objects.filter(csc_id,mac_address)
            registered_devices = DeviceFetch.objects.filter(csc_Id_icontains=csc_id, mac_icontains=mac_address)
            print("register_devices return",registered_devices)
            # for port in ports:
            #     # Check if devices with the provided ports are already registered
            #     print("ports",port,"\n\n")
            #     registered_devices = DeviceFetch.objects.filter(port=port)
        
            # Create a list of device data
            # devices_data = []
            # for device in registered_devices:
            #     devices_data.append({
            #         'ststus': device.status,
            #         'info':device.info,
            #         'port': device.port,
            #         'mi': device.mi,
            #         'dc': device.dc,
            #         'mac': device.mac
            #     })
            # Create a list to store device details
            # Check if registered_devices is empty
            if not registered_devices:
                # Call get_register_device_api to register a new device
                message="Device is not regitered\n**Please register through below link"
                return JsonResponse({'message': message, 'ports':[]}, status=201)
            device_details_list = []
            print("\n\n\nregistered_devices",registered_devices)
            port_list=[]

            for device in registered_devices:
                device_details = f"Device details - port: {device.port}, status: {device.status}, mi: {device.mi}, dc: {device.dc}, mac: {device.mac}"
                device_details_list.append(device_details)
                port_list.append(device.port)

            # Join the list items with a newline character to create a single string
            device_details_string_message = "\n".join(device_details_list)
            # Create a message
            # message = f"Registered devices: {', '.join([str(device['port']) for device in devices_data])}"
            print("message",device_details_string_message)

            # Return device data and message as JSON response
            print("\n\n\nport type",device.port,type(device.port))
            return JsonResponse({'message': device_details_string_message, 'ports':port_list}, status=200)
    except Exception as e:
        # Return error response
        return JsonResponse({'error': str(e)}, status=500)
    

def register_or_update_device_api(request):
    # try:
        if request.method == "POST":
            # Assuming the request body contains the ports array
            print('reque  ',request.body.decode())
            data = json.loads(request.body.decode('utf-8'))
            print("data get registred data", data)
            mac_address = data.get('mac_address')
            ports = data['dev_infos']['ports']
            ports_int = [int(port) for port in ports]
            print("\n\n\nports_int",ports_int)
                
        
            # Check if 'port' and 'mac_address' are present in the request data
            if 'mac_address' in data and 'dev_infos' in data and 'ports' in data['dev_infos']:
                
                
                # Check if csc_Id is present in the database
                csc_id = request.session.get('csc_Id')
                # Check if the number of devices for the csc_Id exceeds the limit
                device_count = DeviceFetch.objects.filter(csc_Id__icontains=csc_id).count()
                if device_count >= 3:
                    return JsonResponse({'error': 'Registration limit exceeded for this CSC ID'}, status=400)

                # for port in ports:
                    # Check if the device with the given port and mac_address already exists
                # Check if the device with the given attributes already exists
                device_exists = DeviceFetch.objects.filter(
                    port=ports,
                    csc_Id__icontains=csc_id,
                    mac__icontains=mac_address,
                    dc=data.get('dev_infos', {}).get('dc'),
                    mi=data.get('dev_infos', {}).get('mi')
                ).exists()

                if device_exists:
                    return JsonResponse({'error': f'Device already registered with this *CSC ID {csc_id}. Please try a different device.'}, status=400)
                else:
                    # Create a new device entry
                    DeviceFetch.objects.create(
                        csc_Id=csc_id,
                        port=8080,
                        status='okay',
                        info='Ready',
                        mi='dummy mi',
                        dc='dummy dc',
                        mac='dummy mac_address',
                        purpose='testing 2'
                    )
                    message = f"Registering new device at port {str(ports)},its Status is {data['dev_infos']['stauts']},and name is {data['dev_infos']['info']}\nDevice registered successfully."
                    print("message",message)
                    return JsonResponse({'message': message, 'ports': ports}, status=200)
            else:
                return JsonResponse({'error': 'Port or mac_address or dev_infos parameter missing'}, status=400)
    # except Exception as e:
    #     return JsonResponse({'error': str(e)}, status=500)
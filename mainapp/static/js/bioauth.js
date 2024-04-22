
// let methodInfo = "";
// let methodCapture = "";
// let finalUrl = '';
// const getCustomDomName = "127.0.0.1";
// let deviceRegistered = false;
// let capture_deviceRegistered=false;

// // window.onload(){
// //     alert("dfg")
// // }

// async function sleep(milliseconds) {
//     return new Promise(resolve => setTimeout(resolve, milliseconds));
// }

// async function discoverAvdm(startPort, endPort, port_8005) {
//     console.log("startPort",startPort,"endPort",endPort);
//     let devices = [];
//     let final_result = {};
//     let i;
//     for (let i = startPort; i <= endPort; i++) 
//     {
//         //const primaryUrl = `http://${getCustomDomName}:`;
//         //let successFlag = false;

//         try {
//             const protocol = window.location.href.includes("https") ? "https://" : "http://";
//             finalUrl = protocol + getCustomDomName + ":" + i.toString();
//         } catch (e) {}

//         let cmbData1 = "";
//         let cmbData2 = "";

//         try {
//             const response = await fetch(finalUrl, { method: "RDSERVICE", cache: "no-cache" });
//             const data = await response.text();
//             const $doc = new DOMParser().parseFromString(data, "text/xml");
//             cmbData1 = $doc.querySelector('RDService').getAttribute('status');
//             cmbData2 = $doc.querySelector('RDService').getAttribute('info');
            
//             if ($doc.querySelector('Interface[path="/rd/capture"]')) {
//                 methodCapture = "/rd/capture";
//             }

//             if ($doc.querySelector('Interface[path="/rd/info"]')) {
//                 methodInfo = "/rd/info";
//             }

//             if (cmbData1 && cmbData2 && methodCapture && methodInfo) {
//                 //successFlag = true;
//                 let result = {};
//                 result = {
//                     raw_xml: { httpStatus: true, data: data },
//                     port: i.toString(),
//                     status: cmbData1,
//                     info: cmbData2,
//                     methodCapture: methodCapture,
//                     methodInfo: methodInfo
//                 };
//                 console.log("port no."+result.port);
//                 devices.push(result);
//             }
//         } catch (error) {
//             final_result["error"] = error.status;
//             // result = { httpStatus: false, err: error.status };
//         }
//     }
//     final_result["devices"] = devices;
//     return final_result;
// }


// async function deviceInfoAvdm(discoveryResult) {
//     let res;
//     let pidData_result;
//     console.log("deviceInfoAvdm(discoveryResult)",discoveryResult);
//     const finalUrl = `http://${getCustomDomName}:${discoveryResult.port}${discoveryResult.methodInfo}`;

//     try {
        
//         const response = await fetch(finalUrl, { method: "DEVICEINFO", cache: "no-cache" });
//         const data = await response.text();
       
//          //Call pid_data function to extract values
//         let pidData = await pid_data(data,false);
//         console.log("pid_data",pidData);
//         pidData_result = {    
//         // Assign values of dpid, rdsid, rdsver, mi, mc, and dc
//         dpid : pidData.dpid,
//         rdsid : pidData.rdsid,
//         rdsver : pidData.rdsver,
//         mi : pidData.mi,
//         mc : pidData.mc,
//         dc : pidData.dc,
//         };
//         console.log("pid data",pidData_result);
//         // deviceRegistered=true;

//         res = { httpStatus: true, data: data, pidData:pidData_result};
//     } catch (error) {
//         res = { httpStatus: false, err: error.status};
//         console.log("error",error);
//     }
//     return res;
// }

// async function captureAvdm(discoveryResult, fCount=1, iCount=0, iType='', fType='',environment="",txtWithaadhar='', txtOtp='', txtClientKey='') {
//     let result = {};
//     let pidData_res ;
//     console.log("environment=>",environment);
//     const strWithaadhar = txtWithaadhar !== '' ? ` wadh="${txtWithaadhar}"` : '';
//     const strOtp = txtOtp !== '' ? ` otp="${txtOtp}"` : '';

//     const XML = `<?xml version="1.0"?>
//         <PidOptions ver="1.0">
//             <Opts fCount="${fCount}" fType="${fType}" iCount="${iCount}" itpye="${iType}" pCount="0" pgCount="0"${strOtp} format="0" 
//                   pidVer="2.0" timeout="20000" pTimeout=""${strWithaadhar} posh="UNKNOWN" env="${environment}" />
//             <CustOpts>
//                 <Param name="ValidationKey" value="${txtClientKey}" />
//             </CustOpts>
//     //     </PidOptions>`;

//     const finalUrl = `http://${getCustomDomName}:${discoveryResult.port}${discoveryResult.methodCapture}`;

//     try {
//         const response = await fetch(finalUrl, {
//             method: "CAPTURE",
//             cache: "no-cache",
//             headers: {
//                 "Content-Type": "text/xml; charset=utf-8"
//             },
//             body: XML
//         });
//         const data = await response.text();

//         // Call pid_data function to extract values
//         let pidData = await pid_data(data,true);
//         pidData_res = {
//         // Assign values of skey->ci, hmac, and data->type
//         skey_ci : pidData.skey_ci,
//         skey_ci_text : pidData.skey_ci_text,
//         hmac : pidData.hmac,
//         data_type : pidData.data_type,
//         data_type_text : pidData.data_type_text,
//         };
//         result = { httpStatus: true, data: data, xml:XML, pidData:pidData_res};


//         const $doc = new DOMParser().parseFromString(data, "text/xml");
//         const message = $doc.querySelector('Resp').getAttribute('errInfo');
//         console.log("error message",message);
//     } catch (error) {
//         result = { httpStatus: false, err: error };
//         console.log("error",error);
//     }
//     //await pid_data(result.data);
//     return result;
// }

// async function pid_data(xml_string,flag) {
//     // Parse the XML string
//     // console.log(xml_string);
// const parser = new DOMParser();
// const xmlDoc = parser.parseFromString(xml_string, "text/xml");
// let pid_results={
// // Get the values of the specified attributes
// dpid: xmlDoc.querySelector("DeviceInfo").getAttribute("dpId"),
// rdsid: xmlDoc.querySelector("DeviceInfo").getAttribute("rdsId"),
// rdsver: xmlDoc.querySelector("DeviceInfo").getAttribute("rdsVer"),
// mi: xmlDoc.querySelector("DeviceInfo").getAttribute("mi"),
// mc: xmlDoc.querySelector("DeviceInfo").getAttribute("mc"),
// dc: xmlDoc.querySelector("DeviceInfo").getAttribute("dc"),
// };
// if (flag) {
//     pid_results = {
//         ...pid_results,
//         skey_ci: xmlDoc.querySelector("Skey").getAttribute("ci"),
//         skey_ci_text: xmlDoc.querySelector("Skey").textContent,
//         hmac: xmlDoc.querySelector("Hmac").textContent,
//         data_type: xmlDoc.querySelector("Data").getAttribute("type"),
//         data_type_text: xmlDoc.querySelector("Data").textContent,
//     }
// }
// // if (xmlDoc.querySelector("Skey")) {
// //     pid_results = {
// //         ...pid_results,
// //         skey_ci: xmlDoc.querySelector("Skey").getAttribute("ci"),
// //         skey_ci_text: xmlDoc.querySelector("Skey").textContent,
// //     }
// // }
// // if (xmlDoc.querySelector("Hmac")) {
// //     pid_results = {
// //         ...pid_results,
// //         hmac: xmlDoc.querySelector("Hmac").textContent,
// //     }
// // }
// // if (xmlDoc.querySelector("Data")) {
// //     pid_results = {
// //         ...pid_results,
// //         data_type: xmlDoc.querySelector("Data").getAttribute("type"),
// //         data_type_text: xmlDoc.querySelector("Data").textContent,
// //     }
// // }
// // Log the extracted values
// console.log("dpid:",  pid_results.dpid);
// console.log("rdsid:",  pid_results.rdsid);
// console.log("rdsver:",  pid_results.rdsver);
// console.log("mi:",  pid_results.mi);
// console.log("mc:",  pid_results.mc);
// console.log("dc:",  pid_results.dc);
// console.log("skey ci:",  pid_results.skey_ci);
// console.log("skey:",  pid_results.skey_ci_text);
// console.log("hmac:",  pid_results.hmac);
// console.log("data type:",  pid_results.data_type);
// console.log("data:",  pid_results.data_type_text);
// return pid_results;
// }


// // Function to get CSRF token from cookie
// function getCookie(name) {
//     let cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         const cookies = document.cookie.split(';');
//         for (let i = 0; i < cookies.length; i++) {
//             const cookie = cookies[i].trim();
//             if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }

// async function globalCapture(start_port,end_port) {
//     console.log("startPort",start_port,"endPort",end_port);
//     // var button = document.getElementById('capture_button');
//     //         button.disabled = true; // Disable the button
//         let discover_dev_info={};
//         let error_message="";
//         let device_index = 0;
//         let ready_devices =await get_ready_devices(start_port,end_port);
//         console.log("ready devices",ready_devices.ready_devices);
        
//         if (ready_devices.ready_devices.length === 0) {
//             if(ready_devices.status=="NOTREADY"){
//                 error_message=`Registered device is not ready found ${start_port === end_port ? '\n*Plese reconnect device registered to this port' + end_port  : ', no active ports/devices found..!!'}`;
//             console.log("Registered device is ready found");
//             }
//             discover_dev_info={
//                 "error_message":error_message,
//                 "process_status":false,
//             };
//             console.log("discover_dev_info",discover_dev_info);
//             return discover_dev_info;
//         }
        
//         else if(ready_devices.ready_devices.length > 1){
//             let device_names = ready_devices.device_names;
//             device_index = prompt(`Which device?\n ${device_names}`);
//             device_index = parseInt(device_index);
            
//             if (isNaN(device_index) || device_index < 0 || device_index >= ready_devices.ready_devices.length) {
//                 console.log("Invalid device index");
//             }
//         }
        
//         console.log("ready devices index=>",device_index);
//         let selected_device = ready_devices.ready_devices[device_index];
//         console.log("selected_device",selected_device);
//         if (selected_device.status !== 'READY') {
//             console.log("Selected device is not ready");
        
//         }
//         else
//         {
//             console.log("capture_deviceRegistered",capture_deviceRegistered);
//             console.log("deviceRegistered",deviceRegistered);
//             if (capture_deviceRegistered===false && deviceRegistered===false)
//             {
//                 document.getElementById('deviceName').value = "("+selected_device["status"]+")"+selected_device["info"];
//             }
        
//         console.log("deviceInfoAvdm(selected_device)",selected_device);
//         const deviceInfoResult = await deviceInfoAvdm(selected_device);
//         console.log("device Info Result:", deviceInfoResult);
        
//         discover_dev_info={
//             "stauts":selected_device.status,
//             "info":selected_device.info,
//             "dc":deviceInfoResult.pidData.dc,
//             "mi":deviceInfoResult.pidData.mi,
//             "ports":selected_device.port,
//         }
//         console.log("selected_device.port",selected_device.port);
//         let captureResult={}
//         console.log("deviceRegistered",deviceRegistered,"\n","capture_deviceRegistered",capture_deviceRegistered);
//         if( deviceRegistered === true && capture_deviceRegistered=== true)
//         {
//             let env = prompt(`Which environment?\n P\nPP\n`);
//             env = String(env); 
//             let fCount = 1, iCount = 0, iType = '',ftype="2";         
//             if(selected_device["info"].includes("Iris")){
//                 fCount = 0, iCount = 1, iType = 'ISO';  
//             }
//             if(env==='P' || env==='PP'){
//             console.log(env);
//             captureResult = await captureAvdm(selected_device,fCount,iCount,iType,ftype,env);
//             console.log("capture Result:", captureResult);
//             }

            

//             console.log("discover_dev_info:-",discover_dev_info)

//         }

//          // Populate textarea fields
//         document.getElementById('device_info').value = deviceInfoResult.data;
//         document.getElementById('Pid_Options').value = captureResult.xml;
//         document.getElementById('Pid_Data').value = captureResult.data;
//         //await pid_data(captureResult.data);
//         // console.log("ready ports",ready_devices.ready_devices.port);
//          // Check if the device is not registered
//         // if (deviceInfoResult.httpStatus === false && deviceRegistered === false) {
//         //     console.log("status",deviceInfoResult.httpStatus,"error",deviceInfoResult.err,"Failed...!! registering new device",discover_dev_info.mi);
//         //     // await capture_using_registered_device(ready_devices.port);
//         //     await globalCapture(start_port,end_port);
//         // }
//         // if (deviceInfoResult.httpStatus === true && deviceRegistered === false) {
//         //     console.log("status",deviceInfoResult.httpStatus,"registering new device",discover_dev_info.mi);
            
//         //     // alert(ready_devices.port);
//         //     await capture_using_registered_device(ready_devices.port,discover_dev_info);
//         //     deviceRegistered = true;

//         // }
//         // }
//     // button.disabled = false; // enable the button
//     return discover_dev_info;
// }}


// async function get_ready_devices(start_port, end_port){
//     let device_results={}
//     let device_names = "";
//     let device;
//     console.log("startPort",start_port,"endPort",end_port);
//     const discoveryResult = await discoverAvdm(start_port, end_port, 8005);
//     console.log("discovery Result",discoveryResult);
//     let ready_devices = [];
//     if(discoveryResult!==undefined && discoveryResult["error"] === undefined && discoveryResult["devices"] !== undefined && discoveryResult["devices"].length > 0)
//     {
//         let devices = discoveryResult["devices"];
//         console.log("devices driver",devices)
//         console.log("devices drivers length",devices.length);
        
//         for(let i=0,j=0; i< devices.length; i++){
        
//             device = devices[i];
//             console.log(i,"drivers",device);
//             console.log(i,"Registered device found:", device["info"],"status:",device["status"]);
//             if(device["status"] === 'READY'){
//                 ready_devices.push(device);
//                 device_names += (j++).toString()+". "+device["info"] +"\n";
//                 console.log("Ready devices found:", device["info"],"status:",device["status"]);
                
//             } 
//          }
//     }
//     else{
//         console.log("Connection Failed")
//         device_results={'error_message':"Connection Failed"};
//     }
//     // Extract ready ports from the ready_devices array
//     const ready_ports = ready_devices.map(device => device.port);

//        // Check if discoveryResult has a 'port' property
   
//         device_results={
//             'ready_devices':ready_devices,
//             'device_names':device_names,
//             'port':ready_ports,
//             'status':device["status"] ,
//         }

//     console.log("device_results",device_results);
//     return device_results;
// }






// async function capture_using_registered_device() {
//     const uniqueId = 2249190931;
    
    
//     // Check if the device is already registered
//     const registeredDevice = await registered_device(uniqueId);
//     console.log("Registered Device:", registeredDevice);
//     if (registeredDevice && Object.keys(registeredDevice).length !== 0){
//         deviceRegistered=true;
//         capture_deviceRegistered=false;
//         // document.getElementById('deviceNameReg').value = ;
//     }
//     else{
//         deviceRegistered=false;
//         capture_deviceRegistered=false;
//     }
//     // let arr_port=registeredDevice.ports
//     // console.log("registeredDevice->ports",registeredDevice.ports);
//     // // alert(arr_port +" "+" "+arr_port.length)
//     // let ports = arr_port.map(item => parseInt(item.replace(/\D/g, '')));

//     // console.log("port arrays",ports);
//     // console.log("length",arr_port.length,"port",ports[0]);


//     let portsStringArray = registeredDevice.ports;
//         // Assuming registeredDevice.ports is an array of strings
        
//     let ports = [];
//     console.log("portsStringArray",portsStringArray);
//     // Iterate over each string in portsStringArray
//     for (let i = 0; i < portsStringArray.length; i++) {
//         let portString = portsStringArray[i];
//         let port = parseInt(portString); // Convert to integer 
//         // let port = parseInt(portString.substring(1, portString.length - 1)); // Remove brackets and convert to integer
//         ports.push(port); // Add the integer port to the ports array
//     }






//     // let start_port=parseInt(arr_port[0]);
//     // let end_port = parseInt(arr_port[arr_port.length - 1]);
//     ports.sort((firstNumber, secondNumber) => firstNumber - secondNumber);// sorts the array in descending order
//     console.log("sorted port array",ports); 
//     let start_port= ports[0];
//     let end_port = ports[portsStringArray.length - 1];
//     // Check if the registered device has ports
//     console.log("deviceRegistered",deviceRegistered);
//     if (registeredDevice && ports.length > 0 && deviceRegistered===true) {
//         console.log("Device is already registered with ports:", start_port );
//         // Call globalCapture with the registered ports
//         // deviceRegistered=true;
//         capture_deviceRegistered=true;
//         let message=await globalCapture(start_port,end_port);
//         // capture_deviceRegistered=true;
//         console.log("message",message);

//         console.log("**Capture using registered device ports:", end_port);
        
//         return `**Capture using registered device ports: ${end_port}`;
//     } else {
//         deviceRegistered=false;
//         capture_deviceRegistered=false;
//         // Device is not registered, return an error message
//         console.log("Device is not registered");
//         console.log(registeredDevice.message);
//         return registeredDevice.message;
//     }
// }

// async function register_New_Device() {
//     debugger;
//     const uniqueId = 2249190931;
//     let message="";
//     // Registering new devices for bio authentication
//     console.log("Registering new devices for bio authentication");
//     const devInfo = await globalCapture(start_port = 11100, end_port = 11106);
//     console.log("Dev Info:", devInfo);
//     console.log("Registering this device with this port:", devInfo.ports);
//     if(devInfo.process_status===false){
//         if(devInfo.error_message!==null){
//             message=devInfo.error_message;
//             console.log("1if Message:",message);
//         }
//         else{
//             message="This ready devices is not registered";
//         console.log("1else message",message);
//         }
//         console.log("Message:",message);
//         deviceRegistered=true;
//         return message;
//     }
//     const deviceRegistered_status = await get_register_device(uniqueId, devInfo);
//     console.log("deviceRegistered_status",deviceRegistered_status);
//     if(deviceRegistered_status["process_status"]===true && deviceRegistered_status["message"]!== undefined){
//     //    if (typeof deviceRegistered_status === 'object' && deviceRegistered_status.error_message && deviceRegistered_status.error_message.length > 0) {
//         message=" Device registered successfully"
//         console.log("2if Message:", message);
//         deviceRegistered=true;
//     }
//     else{
//         message=deviceRegistered_status.error_message;
//         console.log("2else Message:", message);
//     }
    
//   return message;
// }








// // register_device function
// async function get_register_device(mac_address, dev_info) {
//     let message_process_status={};
//     try {
//         // Check if the device is already registered
    
//         console.log("dev_info",dev_info);
//         const checkResponse = await registered_device(mac_address);
//         console.log("checkResponse:-", checkResponse);
//         if (checkResponse.ports.length > 0 && checkResponse.stauts==='READY') {
//             console.log('Device is already registered');
//             console.log(checkResponse.message);
//             return checkResponse.message;
//         }

//         // If the device is not registered, proceed with registration
  
//         const response = await fetch('/register_or_update_device_api/', {
//             method: 'POST',
//             body: JSON.stringify({ mac_address: mac_address, dev_infos: dev_info ,purpose:document.getElementById('inputPurpose').value}),
//             headers: {
//                 'Content-Type': 'application/json',
//                 'X-CSRFToken': getCookie('csrftoken')
//             }
//         });
//         const data = await response.json();
//         console.log("register device", data);
//         let error_message=data["error"];
//         let message=data["message"];
//         // console.log("message",message);
//         console.log("error_message",error_message);
        
//         if(error_message!== undefined && message===undefined){
//             console.log("error message**",error_message);
//             message_process_status={"error_message":error_message,
//                                 "process_status":false}
//             return message_process_status;
//         }
//         else{
//             message_process_status={"message":data.message,"process_status":true};
//             console.log("message_process_status",message_process_status);
//             return message_process_status;
//         }
//     } catch (error) {
//         console.error('Error registering device:', error);
//         return 'Error registering device';
//     }
// }

// // registered_device function
// // async function registered_device(deviceInfo, mac_address, merchant_id) {
//     async function registered_device(mac_address) {
//         try {
//             const response = await fetch('/registered_device_api/', {
//                 method: 'POST',
//                 body: JSON.stringify({ mac_address: mac_address }),
//                 headers: {
//                     'Content-Type': 'application/json',
//                     'X-CSRFToken': getCookie('csrftoken') // Include CSRF token
//                 }
//             });
//             // console.log("un json",response)
//             const data = await response.json();
//             console.log("Registered Device Data:-",data);
//             // alert("regitered devices",data);
//             // Call globalCapture function with the returned data
//             // await globalCapture(data);
//             return data;
//         } catch (error) {
//             console.error('Error checking registered device:', error);
//             return null;
//         }
//     }

//     // async function deRegisterDevice(device) {
//     //     const response = await fetch('/de_register_device/', {
//     //         method: 'POST',
//     //         headers: {
//     //             'Content-Type': 'application/json',
//     //             'X-CSRFToken': getCookie('csrftoken')
//     //         },
            
//     //         body: JSON.stringify({ port: device.port }) // Assuming device has a port property
//     //     });
//     //     console.log("device",device);
//     //     const data = await response.json();
//     //     console.log('De-registration response:', data);
//     //     return data;
//     // }







let methodInfo = "";
let methodCapture = "";
let finalUrl = '';
const getCustomDomName = "127.0.0.1";
let deviceRegistered = false;
let capture_deviceRegistered=false;

// window.onload(){
//     alert("dfg")
// }

async function sleep(milliseconds) {
    return new Promise(resolve => setTimeout(resolve, milliseconds));
}

async function discoverAvdm(startPort, endPort, port_8005) {
    console.log("startPort",startPort,"endPort",endPort);
    let devices = [];
    let final_result = {};
    let i;
    for (let i = startPort; i <= endPort; i++) 
    {
        //const primaryUrl = `http://${getCustomDomName}:`;
        //let successFlag = false;

        try {
            const protocol = window.location.href.includes("https") ? "https://" : "http://";
            finalUrl = protocol + getCustomDomName + ":" + i.toString();
        } catch (e) {}

        let cmbData1 = "";
        let cmbData2 = "";

        try {
            const response = await fetch(finalUrl, { method: "RDSERVICE", cache: "no-cache" });
            const data = await response.text();
            const $doc = new DOMParser().parseFromString(data, "text/xml");
            cmbData1 = $doc.querySelector('RDService').getAttribute('status');
            cmbData2 = $doc.querySelector('RDService').getAttribute('info');
            
            if ($doc.querySelector('Interface[path="/rd/capture"]')) {
                methodCapture = "/rd/capture";
            }

            if ($doc.querySelector('Interface[path="/rd/info"]')) {
                methodInfo = "/rd/info";
            }

            if (cmbData1 && cmbData2 && methodCapture && methodInfo) {
                //successFlag = true;
                let result = {};
                result = {
                    raw_xml: { httpStatus: true, data: data },
                    port: i.toString(),
                    status: cmbData1,
                    info: cmbData2,
                    methodCapture: methodCapture,
                    methodInfo: methodInfo
                };
                console.log("port no."+result.port);
                devices.push(result);
            }
        } catch (error) {
            final_result["error"] = error.status;
            // result = { httpStatus: false, err: error.status };
        }
    }
    final_result["devices"] = devices;
    return final_result;
}


async function deviceInfoAvdm(discoveryResult) {
    let res;
    let pidData_result;
    console.log("deviceInfoAvdm(discoveryResult)",discoveryResult);
    const finalUrl = `http://${getCustomDomName}:${discoveryResult.port}${discoveryResult.methodInfo}`;

    try {
        
        const response = await fetch(finalUrl, { method: "DEVICEINFO", cache: "no-cache" });
        const data = await response.text();
       
         //Call pid_data function to extract values
        let pidData = await pid_data(data,false);
        console.log("pid_data",pidData);
        pidData_result = {    
        // Assign values of dpid, rdsid, rdsver, mi, mc, and dc
        dpid : pidData.dpid,
        rdsid : pidData.rdsid,
        rdsver : pidData.rdsver,
        mi : pidData.mi,
        mc : pidData.mc,
        dc : pidData.dc,
        };
        console.log("pid data",pidData_result);
        
        res = { httpStatus: true, data: data, pidData:pidData_result};
    } catch (error) {
        res = { httpStatus: false, err: error.status};
        console.log("error",error);
    }
    return res;
}

async function captureAvdm(discoveryResult, fCount=1, iCount=0, iType='', fType='',environment="",txtWithaadhar='', txtOtp='', txtClientKey='') {
    let result = {};
    let pidData_res ;
    console.log("environment=>",environment);
    const strWithaadhar = txtWithaadhar !== '' ? ` wadh="${txtWithaadhar}"` : '';
    const strOtp = txtOtp !== '' ? ` otp="${txtOtp}"` : '';

    const XML = `<?xml version="1.0"?>
        <PidOptions ver="1.0">
            <Opts fCount="${fCount}" fType="${fType}" iCount="${iCount}" itpye="${iType}" pCount="0" pgCount="0"${strOtp} format="0" 
                  pidVer="2.0" timeout="20000" pTimeout=""${strWithaadhar} posh="UNKNOWN" env="${environment}" />
            <CustOpts>
                <Param name="ValidationKey" value="${txtClientKey}" />
            </CustOpts>
    //     </PidOptions>`;

    const finalUrl = `http://${getCustomDomName}:${discoveryResult.port}${discoveryResult.methodCapture}`;

    try {
        const response = await fetch(finalUrl, {
            method: "CAPTURE",
            cache: "no-cache",
            headers: {
                "Content-Type": "text/xml; charset=utf-8"
            },
            body: XML
        });
        const data = await response.text();

        // Call pid_data function to extract values
        let pidData = await pid_data(data,true);
        pidData_res = {
        // Assign values of skey->ci, hmac, and data->type
        skey_ci : pidData.skey_ci,
        skey_ci_text : pidData.skey_ci_text,
        hmac : pidData.hmac,
        data_type : pidData.data_type,
        data_type_text : pidData.data_type_text,
        };
        result = { httpStatus: true, data: data, xml:XML, pidData:pidData_res};


        const $doc = new DOMParser().parseFromString(data, "text/xml");
        const message = $doc.querySelector('Resp').getAttribute('errInfo');
        console.log("error message",message);
    } catch (error) {
        result = { httpStatus: false, err: error };
        console.log("error",error);
    }
    //await pid_data(result.data);
    return result;
}

async function pid_data(xml_string,flag) {
    // Parse the XML string
    // console.log(xml_string);
const parser = new DOMParser();
const xmlDoc = parser.parseFromString(xml_string, "text/xml");
let pid_results={
// Get the values of the specified attributes
dpid: xmlDoc.querySelector("DeviceInfo").getAttribute("dpId"),
rdsid: xmlDoc.querySelector("DeviceInfo").getAttribute("rdsId"),
rdsver: xmlDoc.querySelector("DeviceInfo").getAttribute("rdsVer"),
mi: xmlDoc.querySelector("DeviceInfo").getAttribute("mi"),
mc: xmlDoc.querySelector("DeviceInfo").getAttribute("mc"),
dc: xmlDoc.querySelector("DeviceInfo").getAttribute("dc"),
};
if (flag) {
    pid_results = {
        ...pid_results,
        skey_ci: xmlDoc.querySelector("Skey").getAttribute("ci"),
        skey_ci_text: xmlDoc.querySelector("Skey").textContent,
        hmac: xmlDoc.querySelector("Hmac").textContent,
        data_type: xmlDoc.querySelector("Data").getAttribute("type"),
        data_type_text: xmlDoc.querySelector("Data").textContent,
    }
}
// if (xmlDoc.querySelector("Skey")) {
//     pid_results = {
//         ...pid_results,
//         skey_ci: xmlDoc.querySelector("Skey").getAttribute("ci"),
//         skey_ci_text: xmlDoc.querySelector("Skey").textContent,
//     }
// }
// if (xmlDoc.querySelector("Hmac")) {
//     pid_results = {
//         ...pid_results,
//         hmac: xmlDoc.querySelector("Hmac").textContent,
//     }
// }
// if (xmlDoc.querySelector("Data")) {
//     pid_results = {
//         ...pid_results,
//         data_type: xmlDoc.querySelector("Data").getAttribute("type"),
//         data_type_text: xmlDoc.querySelector("Data").textContent,
//     }
// }
// Log the extracted values
console.log("dpid:",  pid_results.dpid);
console.log("rdsid:",  pid_results.rdsid);
console.log("rdsver:",  pid_results.rdsver);
console.log("mi:",  pid_results.mi);
console.log("mc:",  pid_results.mc);
console.log("dc:",  pid_results.dc);
console.log("skey ci:",  pid_results.skey_ci);
console.log("skey:",  pid_results.skey_ci_text);
console.log("hmac:",  pid_results.hmac);
console.log("data type:",  pid_results.data_type);
console.log("data:",  pid_results.data_type_text);
return pid_results;
}


// Function to get CSRF token from cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

async function globalCapture(start_port,end_port) {
    console.log("startPort",start_port,"endPort",end_port);
    // var button = document.getElementById('capture_button');
    //         button.disabled = true; // Disable the button
        let discover_dev_info={};
        let error_message="";
        let device_index = 0;
        let ready_devices =await get_ready_devices(start_port,end_port);
        console.log("ready devices",ready_devices.ready_devices);
        
        if (ready_devices.ready_devices.length === 0) {
            if(ready_devices.status=="NOTREADY"){
                error_message=`Registered device is not ready found ${start_port === end_port ? '\n*Plese reconnect device registered to this port' + end_port  : ', no active ports/devices found..!!'}`;
            console.log("Registered device is ready found");
            }
            discover_dev_info={
                "error_message":error_message,
                "process_status":false,
            };
            console.log("discover_dev_info",discover_dev_info);
            return discover_dev_info;
        }
        
        else if(ready_devices.ready_devices.length > 1){
            let device_names = ready_devices.device_names;
            device_index = prompt(`Which device?\n ${device_names}`);
            device_index = parseInt(device_index);
            
            if (isNaN(device_index) || device_index < 0 || device_index >= ready_devices.ready_devices.length) {
                console.log("Invalid device index");
            }
        }
        
        console.log("ready devices index=>",device_index);
        let selected_device = ready_devices.ready_devices[device_index];
        console.log("selected_device",selected_device);
        if (selected_device.status !== 'READY') {
            console.log("Selected device is not ready");
        
        }
        else
        {
            console.log("capture_deviceRegistered",capture_deviceRegistered);
            console.log("deviceRegistered",deviceRegistered);
            if (capture_deviceRegistered===false && deviceRegistered===false)
            {
                document.getElementById('deviceName').value = "("+selected_device["status"]+")"+selected_device["info"];
            }
        
        console.log("deviceInfoAvdm(selected_device)",selected_device);
        const deviceInfoResult = await deviceInfoAvdm(selected_device);
        console.log("device Info Result:", deviceInfoResult);
        
        discover_dev_info={
            "stauts":selected_device.status,
            "info":selected_device.info,
            "dc":deviceInfoResult.pidData.dc,
            "mi":deviceInfoResult.pidData.mi,
            "ports":selected_device.port,
        }
        console.log("selected_device.port",selected_device.port);
        let captureResult={}
        console.log("deviceRegistered",deviceRegistered,"\n","capture_deviceRegistered",capture_deviceRegistered);
        if( deviceRegistered === true && capture_deviceRegistered=== true)
        {
            let env = prompt(`Which environment?\n P\nPP\n`);
            env = String(env); 
            let fCount = 1, iCount = 0, iType = '',ftype="2";         
            if(selected_device["info"].includes("Iris")){
                fCount = 0, iCount = 1, iType = 'ISO';  
            }
            if(env==='P' || env==='PP'){
            console.log(env);
            captureResult = await captureAvdm(selected_device,fCount,iCount,iType,ftype,env);
            console.log("capture Result:", captureResult);
            }

            

            console.log("discover_dev_info:-",discover_dev_info)

        }
        console.log("captureResult.xml:-",captureResult.xml);
         // Populate textarea fields
        document.getElementById('device_info').value = deviceInfoResult.data;
        document.getElementById('Pid_Options').value = captureResult.xml;
        document.getElementById('Pid_Data').value = captureResult.data;
    return discover_dev_info;
}}


async function get_ready_devices(start_port, end_port){
    let device_results={}
    let device_names = "";
    let device;
    console.log("startPort",start_port,"endPort",end_port);
    const discoveryResult = await discoverAvdm(start_port, end_port, 8005);
    console.log("discovery Result",discoveryResult);
    let ready_devices = [];
    if(discoveryResult!==undefined && discoveryResult["error"] === undefined && discoveryResult["devices"] !== undefined && discoveryResult["devices"].length > 0)
    {
        let devices = discoveryResult["devices"];
        console.log("devices driver",devices)
        console.log("devices drivers length",devices.length);
        
        for(let i=0,j=0; i< devices.length; i++){
        
            device = devices[i];
            console.log(i,"drivers",device);
            console.log(i,"Registered device found:", device["info"],"status:",device["status"]);
            if(device["status"] === 'READY'){
                ready_devices.push(device);
                device_names += (j++).toString()+". "+device["info"] +"\n";
                console.log("Ready devices found:", device["info"],"status:",device["status"]);
                
            } 
         }
    }
    else{
        console.log("Connection Failed")
        device_results={'error_message':"Connection Failed"};
    }
    // Extract ready ports from the ready_devices array
    const ready_ports = ready_devices.map(device => device.port);

       // Check if discoveryResult has a 'port' property
   
        device_results={
            'ready_devices':ready_devices,
            'device_names':device_names,
            'port':ready_ports,
            'status':device["status"] ,
        }

    console.log("device_results",device_results);
    return device_results;
}






async function capture_using_registered_device() {
    const uniqueId = 2249190931;
    
    
    // Check if the device is already registered
    const registeredDevice = await registered_device();
    console.log("Registered Device:", registeredDevice);
    if (registeredDevice && Object.keys(registeredDevice).length !== 0){
        deviceRegistered=true;
        capture_deviceRegistered=false;
        // document.getElementById('deviceNameReg').value = ;
    }
    else{
        deviceRegistered=false;
        capture_deviceRegistered=false;
    }
    // let arr_port=registeredDevice.ports
    // console.log("registeredDevice->ports",registeredDevice.ports);
    // // alert(arr_port +" "+" "+arr_port.length)
    // let ports = arr_port.map(item => parseInt(item.replace(/\D/g, '')));

    // console.log("port arrays",ports);
    // console.log("length",arr_port.length,"port",ports[0]);


    let portsStringArray = registeredDevice.ports;
        // Assuming registeredDevice.ports is an array of strings
        
    let ports = [];
    console.log("portsStringArray",portsStringArray);
    // Iterate over each string in portsStringArray
    for (let i = 0; i < portsStringArray.length; i++) {
        let portString = portsStringArray[i];
        let port = parseInt(portString); // Convert to integer 
        // let port = parseInt(portString.substring(1, portString.length - 1)); // Remove brackets and convert to integer
        ports.push(port); // Add the integer port to the ports array
    }






    // let start_port=parseInt(arr_port[0]);
    // let end_port = parseInt(arr_port[arr_port.length - 1]);
    ports.sort((firstNumber, secondNumber) => firstNumber - secondNumber);// sorts the array in descending order
    console.log("sorted port array",ports); 
    let start_port= ports[0];
    let end_port = ports[portsStringArray.length - 1];
    // Check if the registered device has ports
    console.log("deviceRegistered",deviceRegistered);
    if (registeredDevice && ports.length > 0 && deviceRegistered===true) {
        console.log("Device is already registered with ports:", start_port );
        // Call globalCapture with the registered ports
        // deviceRegistered=true;
        capture_deviceRegistered=true;
        let message=await globalCapture(start_port,end_port);
        // capture_deviceRegistered=true;
        console.log("message",message);

        console.log("**Capture using registered device ports:", end_port);
        
        return `**Capture using registered device ports: ${end_port}`;
    } else {
        deviceRegistered=false;
        capture_deviceRegistered=false;
        // Device is not registered, return an error message
        console.log("Device is not registered");
        console.log(registeredDevice.message);
        return registeredDevice.message;
    }
}

async function register_New_Device() {
    // debugger;
    // const uniqueId = 2249190931;
    let message="";
    // Registering new devices for bio authentication
    console.log("Registering new devices for bio authentication");
    const devInfo = await globalCapture(start_port = 11100, end_port = 11106);
    console.log("Dev Info:", devInfo);
    console.log("Registering this device with this port:", devInfo.ports);
    if(devInfo.process_status===false){
        if(devInfo.error_message!==null){
            message=devInfo.error_message;
            console.log("1if Message:",message);
        }
        else{
            message="This ready devices is not registered";
        console.log("1else message",message);
        }
        console.log("Message:",message);
        deviceRegistered=false;
        return message;
    }
    const deviceRegistered_status = await get_register_device(devInfo);
    console.log("deviceRegistered_status",deviceRegistered_status);
    if(deviceRegistered_status["process_status"]===true && deviceRegistered_status["message"]!== undefined){
        message=" Device registered successfully"
        console.log("2if Message:", message);
        deviceRegistered=true;
    }
    else{
        message=deviceRegistered_status.error_message;
        console.log("2else Message:", message);
    }
    
  return message;
}








// register_device function
async function get_register_device(dev_info) {
    let message_process_status={};
    // try {
        // Check if the device is already registered
    
        console.log("dev_info",dev_info);
        const checkResponse = await registered_device();
        console.log("checkResponse:-", checkResponse);
        if (checkResponse.ports.length > 0 && checkResponse.stauts==='READY') {
            console.log('Device is already registered');
            console.log(checkResponse.message);
            return checkResponse.message;
        }

        // If the device is not registered, proceed with registration
        console.log("dev_info............\n",dev_info,"purpose...........",document.getElementById('inputPurpose').value);
        const response = await fetch('/register_or_update_device_api/', {
            method: 'POST',
            body: JSON.stringify({'dev_infos': dev_info ,'purpose':document.getElementById('inputPurpose').value}),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
        });
        const data = await response.json();
        console.log("register device", data);
        let error_message=data["error"];
        let message=data["message"];
        // console.log("message",message);
        console.log("error_message",error_message);
        
        if(error_message!== undefined && message===undefined){
            console.log("error message**",error_message);
            message_process_status={"error_message":error_message,
                                "process_status":false}
            return message_process_status;
        }
        else{
            message_process_status={"message":data.message,"process_status":true};
            console.log("message_process_status",message_process_status);
            return message_process_status;
        }
    // } catch (error) {
    //     console.error('Error registering device:', error);
    //     return 'Error registering device';
    // }
}

// registered_device function
// async function registered_device(deviceInfo, mac_address, merchant_id) {
    async function registered_device() {
        try {
            const response = await fetch('/registered_device_api/', {
                method: 'POST',
                body: JSON.stringify({ }),
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken') // Include CSRF token
                }
            });
            // console.log("un json",response)
            const data = await response.json();
            console.log("Registered Device Data:-",data);
            // alert("regitered devices",data);
            // Call globalCapture function with the returned data
            // await globalCapture(data);
            return data;
        } catch (error) {
            console.error('Error checking registered device:', error);
            return null;
        }
    }

    // async function deRegisterDevice(device) {
    //     const response = await fetch('/de_register_device/', {
    //         method: 'POST',
    //         headers: {
    //             'Content-Type': 'application/json',
    //             'X-CSRFToken': getCookie('csrftoken')
    //         },
            
    //         body: JSON.stringify({ port: device.port }) // Assuming device has a port property
    //     });
    //     console.log("device",device);
    //     const data = await response.json();
    //     console.log('De-registration response:', data);
    //     return data;
    // }
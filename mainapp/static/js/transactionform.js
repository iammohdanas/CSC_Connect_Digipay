let methodInfo = "";
let methodCapture = "";
let finalUrl = '';
const getCustomDomName = "127.0.0.1";

async function sleep(milliseconds) {
    return new Promise(resolve => setTimeout(resolve, milliseconds));
}

async function discoverAvdm(startPort, endPort, port8005) {
    let devices = [];
    let final_result = {};
    for (let i = startPort; i <= endPort; i++) {
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
    const finalUrl = `http://${getCustomDomName}:${discoveryResult.port}${discoveryResult.methodInfo}`;

    try {
        // debugger;
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

        res = { httpStatus: true, data: data, pidData:pidData_result };
    } catch (error) {
        res = { httpStatus: false, err: error.status};
        console.log("error",error);
    }
    return res;
}

async function captureAvdm(discoveryResult, fCount=1, iCount=0, iType='', txtWithaadhar='', txtOtp='', txtClientKey='') {
    let result = {};
    let pidData_res ;
    const strWithaadhar = txtWithaadhar !== '' ? ` wadh="${txtWithaadhar}"` : '';
    const strOtp = txtOtp !== '' ? ` otp="${txtOtp}"` : '';

    const XML = `<?xml version="1.0"?>
        <PidOptions ver="1.0">
            <Opts fCount="${fCount}" fType="2" iCount="${iCount}" itpye="${iType}" pCount="0" pgCount="0"${strOtp} format="0" 
                pidVer="2.0" timeout="20000" pTimeout=""${strWithaadhar} posh="UNKNOWN" env="P" />
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
        result = { httpStatus: false, err: error.status };
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

function enableProceedButton() {
    document.getElementById('proceed_button').disabled = false;
}



async function globalCapture() {
    var button = document.getElementById('capture_button');
    button.disabled = true; // Disable the button
    const discoveryResult = await discoverAvdm(11100, 11106, 8005);
    console.log(discoveryResult);
    if(discoveryResult!==undefined && discoveryResult["error"] === undefined && discoveryResult["devices"] !== undefined && discoveryResult["devices"].length > 0)
    {
        let devices = discoveryResult["devices"];
        let ready_devices = [];
        let device_names = "";
        for(let i=0,j=0; i< devices.length; i++){
            let device = devices[i];
            if(device["status"] === 'READY'){
                ready_devices.push(device)
                device_names += (j++).toString()+". "+device["info"] +"\n";
            } 
        }
        let device_index = 0;
        if(ready_devices.length > 1){
            device_index = prompt(`Which device?\n ${device_names}`);
            device_index = parseInt(device_index);
        }
        const deviceInfoResult = await deviceInfoAvdm(ready_devices[device_index]);
        console.log("device Info Result:", deviceInfoResult);
        let selected_device = ready_devices[device_index];
        let fCount = 1, iCount = 0, iType = '';         
        if(selected_device["info"].includes("Iris")){
            fCount = 0, iCount = 1, iType = 'ISO';  
        }
        const captureResult = await captureAvdm(selected_device,fCount,iCount,iType);
        console.log("capture Result:", captureResult);

        // Populate textarea fields
        document.getElementById('device_info').value = deviceInfoResult.data;
        document.getElementById('Pid Options').value = captureResult.xml;
        document.getElementById('Pid Data').value = captureResult.data;
        //await pid_data(captureResult.data);

        document.getElementById('authentication_message').innerText = "Authentication Successful";
        document.getElementById('authentication_message').style.color = "green";        
        
    }
    else{
        console.log("Connection Failed")
        document.getElementById('authentication_message').innerText = "Authentication Failed";
        document.getElementById('authentication_message').style.color = "red";
    }
    document.getElementById('authentication_message').style.display = 'block';
    button.disabled = false; // enable the button
    enableProceedButton();
}

//for progressive fields
document.addEventListener("DOMContentLoaded", function() {
    var transactionTypeSelect = document.getElementById("withdrawformtransactionType");
    var customerMobileNumberField = document.getElementById("customerMobileNumberField");
    var aadharNumberField = document.getElementById("aadharNumberField");
    var amountField = document.getElementById("amountField");
    var bankOptionField = document.getElementById("bankOptionField");
    var authdevregister =  document.getElementById("authdevregister");
    var aadharInput = document.getElementById("withdrawformaadharNumber");
    var mobileInput = document.getElementById("withdrawformcustomerMobileNumber");
    var amountInput =  document.getElementById("withdrawformamount");
    var deviceinfo =  document.getElementById("device_info");
    var pidOptions =  document.getElementById("Pid Options");
    var pidData =  document.getElementById("Pid Data");

    deviceinfo.style.display = "none";
    pidOptions.style.display = "none";
    pidData.style.display = "none";
    

    function clearFields() {
        document.getElementById("withdrawformcustomerMobileNumber").value = "";
        document.getElementById("withdrawformaadharNumber").value = "";
        document.getElementById("withdrawformamount").value = "";
        document.getElementById("withdrawformbankOption").selectedIndex  = 0;
    }
    function toggleFields() {
        var selectedTransactionType = transactionTypeSelect.value;

        if (selectedTransactionType === "22" ||
            selectedTransactionType === "23" ||
            selectedTransactionType === "24") {
            customerMobileNumberField.style.display = "block";
            aadharNumberField.style.display = "block";
            bankOptionField.style.display = "block";
            amountField.style.display = "block";
            authdevregister.style.display = "block";
            enableFields();
            clearFields();
        } else if (selectedTransactionType === "26") {
            customerMobileNumberField.style.display = "none";
            aadharNumberField.style.display = "block";
            bankOptionField.style.display = "block";
            amountField.style.display = "block";
            authdevregister.style.display = "block";
            clearFields();
        } else {
            customerMobileNumberField.style.display = "none";
            aadharNumberField.style.display = "none";
            bankOptionField.style.display = "none";
            amountField.style.display = "none";
            authdevregister.style.display = "none";
            clearFields();
            disableFields();
        }
    }

    toggleFields();
    transactionTypeSelect.addEventListener("change", toggleFields);

    function disableFields() {
        aadharInput.disabled = true;
        mobileInput.disabled = true;
        amountInput.disabled = true;
    }
    
    function enableAadharField() {
        aadharInput.disabled = false;
        aadharInput.focus();
    }
    

    function enableMobileField() {
        if (aadharInput.value.length === 12 && validateAadhar(aadharInput.value)) {
            mobileInput.disabled = false;
            mobileInput.focus();
        } else {
            mobileInput.disabled = true;
            amountInput.disabled = true;
        }
    }

    function validateAadhar(aadharNumber) {
        const d = [
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            [1, 2, 3, 4, 0, 6, 7, 8, 9, 5], 
            [2, 3, 4, 0, 1, 7, 8, 9, 5, 6], 
            [3, 4, 0, 1, 2, 8, 9, 5, 6, 7], 
            [4, 0, 1, 2, 3, 9, 5, 6, 7, 8], 
            [5, 9, 8, 7, 6, 0, 4, 3, 2, 1], 
            [6, 5, 9, 8, 7, 1, 0, 4, 3, 2], 
            [7, 6, 5, 9, 8, 2, 1, 0, 4, 3], 
            [8, 7, 6, 5, 9, 3, 2, 1, 0, 4], 
            [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
          ]
          const p = [
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 
            [1, 5, 7, 6, 2, 8, 3, 0, 9, 4], 
            [5, 8, 0, 3, 7, 9, 6, 1, 4, 2], 
            [8, 9, 1, 6, 0, 4, 3, 5, 2, 7], 
            [9, 4, 5, 3, 1, 2, 6, 8, 7, 0], 
            [4, 2, 8, 6, 5, 7, 3, 9, 0, 1], 
            [2, 7, 9, 3, 8, 0, 6, 4, 1, 5], 
            [7, 0, 4, 6, 9, 1, 3, 2, 5, 8]
          ]
          let c = 0
            let invertedArray = aadharNumber.split('').map(Number).reverse()

            invertedArray.forEach((val, i) => {
                c = d[c][p[(i % 8)][val]]
            })
            return (c === 0)
    }

    function enableAmountField() {
        var mobileNumberPattern = /^[6789][0-9]{9}$/;
        if (mobileInput.value.length === 10) {
            if (!mobileNumberPattern.test(mobileInput.value)) {
                document.getElementById("errorText").style.display = "block";
                amountInput.disabled = true;
            } else {
                document.getElementById("errorText").style.display = "none";
                amountInput.disabled = false;
                amountInput.focus();
            }
        } else {
            amountInput.disabled = true;
        }
    }
    transactionTypeSelect.addEventListener("change", toggleFields);
    bankOptionField.addEventListener("change", enableAadharField);
    aadharInput.addEventListener("input", enableMobileField);
    mobileInput.addEventListener("input", enableAmountField);
});

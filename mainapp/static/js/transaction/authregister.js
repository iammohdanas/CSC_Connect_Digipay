var devicename = document.getElementById("deviceName");
var inputpurpose = document.getElementById("inputPurpose");
var register = document.getElementById("registerbioauth");

function disableFields() {
    inputpurpose.disabled = true;
    register.disabled = true;
}

function enablePurposeField() {
    if (devicename.value.trim().length >= 6) {
        inputpurpose.disabled = false;
    } else {
        inputpurpose.disabled = true;
        register.disabled = true;
    }
}

function enableRegisterBioAuthbutton(){
    if(inputpurpose.value.trim().length >= 12){
        register.disabled = false;
    } else {
        register.disabled = true;
    }
}

disableFields(); // Initially disable fields
devicename.addEventListener('input', enablePurposeField);
inputpurpose.addEventListener('input', enableRegisterBioAuthbutton);
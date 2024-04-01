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

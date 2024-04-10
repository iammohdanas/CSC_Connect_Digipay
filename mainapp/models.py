from django.db import models

# Create your models here.
class Transaction(models.Model):
    txn_id = models.CharField(max_length=100, verbose_name="Transaction ID", primary_key=True)
    timestamp = models.DateTimeField(verbose_name="Timestamp")
    customer_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="Customer ID")
    aadhaar_number = models.CharField(max_length=100, verbose_name="Aadhaar Number")
    transaction_type = models.CharField(max_length=100, verbose_name="Transaction Type")
    transaction_amount_value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Transaction Amount Value")
    transaction_amount_currency = models.CharField(max_length=3, verbose_name="Transaction Amount Currency")
    transaction_status = models.CharField(max_length=100, blank=True, null=True, verbose_name="Transaction Status")
    error_code = models.CharField(max_length=100, blank=True, null=True, verbose_name="Error Code")
    merchant_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="Merchant ID")
    terminal_id = models.CharField(max_length=100, verbose_name="Terminal ID")
    bank_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="Bank ID")
    location = models.CharField(max_length=100, verbose_name="Location")
    transaction_ref_number = models.CharField(max_length=100, verbose_name="Transaction Reference Number", unique=True)
    response_code = models.CharField(max_length=100, blank=True, null=True, verbose_name="Response Code")
    remarks = models.TextField(blank=True, null=True, verbose_name="Remarks")
    user_agent = models.TextField(blank=True, null=True, verbose_name="User Agent")
    transaction_fee = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Transaction Fee")
    customer_reference_number = models.CharField(max_length=100, verbose_name="Customer Reference Number",null=True, unique=True)


class DeviceFetch(models.Model):
    id=models.AutoField(primary_key=True)
    port = models.TextField()
    status = models.CharField(max_length=20,null=True)
    info = models.CharField(max_length=200,null=True)
    dc = models.CharField(max_length=100,null=True)
    mi = models.CharField(max_length=100,null=True)
    mac = models.CharField(max_length=100,null=True)
    csc_Id = models.CharField(max_length=100,null=True)
    purpose = models.CharField(max_length=300,null=True)
    # Add more fields as needed
    def __str__(self):
        return f"DeviceFetch(id={self.id} ,port={self.port}, status={self.status}),info={self.info}, dc={self.dc},mi={self.mi},mac={self.mac},csc_id={self.csc_Id},purpose={self.purpose}"

class DeviceAuth(models.Model):
    csc_id = models.CharField(max_length=200, primary_key=True)
    device_id = models.CharField(max_length=100,null=True)
    # port = models.ForeignKey(DeviceFetch, on_delete=models.CASCADE, related_name='authentications',null=True)
    hmac = models.CharField(max_length=20,null=True)

class DeviceRegister(models.Model):
    device_name = models.CharField(max_length=100,null=True)
    purpose = models.CharField(max_length=300,null=True)
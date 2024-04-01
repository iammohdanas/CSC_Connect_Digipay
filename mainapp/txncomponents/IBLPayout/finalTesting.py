from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import secrets
import json
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import json
import base64
import requests

def generate_key(length=32):
    # Generate a 32-byte (256-bit) key
    aes_key = secrets.token_bytes(length)
    return aes_key

def encrypt_aes_key_with_rsa(public_key, aes_key):
    # Encrypt AES key using RSA-OAEP
    cipher_rsa = PKCS1_OAEP.new(public_key)
    encrypted_aes_key = cipher_rsa.encrypt(aes_key)
    return encrypted_aes_key

def encrypt_data(data, key):
    iv = get_random_bytes(16)
    cipher_aes = AES.new(key, AES.MODE_CBC, iv)
    ct_bytes = cipher_aes.encrypt(pad(json.dumps(data).encode(), AES.block_size))
    encrypted_data = base64.b64encode(iv + ct_bytes).decode('utf-8')
    return encrypted_data

def decrypt_data( encrypted_data):
        decoded_data = base64.b64decode(encrypted_data.encode('utf-8'))
        iv = decoded_data[:16]  # Extract IV
        ciphertext = decoded_data[16:]  # Extract ciphertext
        cipher_aes = AES.new(key, AES.MODE_CBC, iv)
        decrypted_data = unpad(cipher_aes.decrypt(ciphertext), AES.block_size).decode('utf-8')
        return json.loads(decrypted_data)

def decrypt_response(encrypted_data, encrypted_aes_key_with_rsa):
    encrypted_data = base64.b64decode(encrypted_data)
    key = base64.b64decode(encrypted_aes_key_with_rsa)
    iv = encrypted_data[:16]
    ciphertext = encrypted_data[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
    return decrypted_data



public_key_pem = """-----BEGIN CERTIFICATE-----
MIIDojCCAoqgAwIBAgIIBmMSCJVcNv4wDQYJKoZIhvcNAQELBQAwOzELMAkGA1UE
BhMCSU4xETAPBgNVBAoMCGluZHVzaW5kMRkwFwYDVQQDDBBpbmR1c2luZC1lbmMt
ZGVjMB4XDTIyMDcxMjA3NDAxMVoXDTMyMDcwOTA3NDAxMVowOzELMAkGA1UEBhMC
SU4xETAPBgNVBAoMCGluZHVzaW5kMRkwFwYDVQQDDBBpbmR1c2luZC1lbmMtZGVj
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAu60AzxMOMrBQ4zrsyh4y
ftU82X+bUz5NqVAa7kvrHJQVawqfQJiI6T72tFDULHxyiBXu+zOmPQH9WGIk9Rri
IIAUT6iRKtmLfk7ihZkVoYSbvN3mKFAhOGghBJmlJeEL301yhU38y2Nu/nx0mm/Y
/r5DsSAzhet+U5GNBL8fYo0uOZ9Ooziuv9h+nqX0u2tcIPJmausesw42ceXXDJul
YjHOMIRg8cyidWSIYLEdebxocOzXuq9hcpoxF45F5br9+syYuQSqzSYDj02xRcee
nU/rh78Al4cRcYDTmQ6OrZL+OrAcUjiqkR+mX+QKPI5vpo4I5cQMIzkSg+SQFevW
BwIDAQABo4GpMIGmMAwGA1UdEwQFMAMBAf8wHQYDVR0OBBYEFDlKyoJrELE0Ftrz
WSdZQNTGzCEYMGoGA1UdIwRjMGGAFDlKyoJrELE0FtrzWSdZQNTGzCEYoT+kPTA7
MQswCQYDVQQGEwJJTjERMA8GA1UECgwIaW5kdXNpbmQxGTAXBgNVBAMMEGluZHVz
aW5kLWVuYy1kZWOCCAZjEgiVXDb+MAsGA1UdDwQEAwICvDANBgkqhkiG9w0BAQsF
AAOCAQEAs3VlD7kLZZ7TH9S4KGm5s+5feJdl7Xnjq1f+GE8lSKC7hPgHoeiCHb2r
7TNWHszhHvBfMfYXPk0Pb60q2VaDZYQbcaetoZsyP33/S/ZxjMIL3KVb9sp7kMXI
JTby+SqXNxAipoO0RJapiaEBidOgRspYFAjjgeGGvmmxU6yLIsSM12jIxGSm0Mrd
zzEkzOMADlPj4TW8Mwo7rSls7nQ120qJTZRwpqu2FsiSxk4Krt/L0WbIjzXjnxqQ
O1sDVzmo0g35a0+MhfFJvsJFJ4GcLu+s22GPXYvVMXn6WFcxgW/CN2LggO1VDYCs
bmJIfMS8JWis0fdzPkCdPXWZvIY7OQ==
-----END CERTIFICATE-----
"""

# Load the RSA public key



data = {
    'Customerid': '1234567890',
    'Transaction Type': 'DEBIT',
    'CustomerRefNumber': 'REF123',
    'DebitAccountNo': '1234567890123',
    'BeneficiaryName': 'John Doe',
    'CreditAccountNumber': '9876543210987',
    'BeneficiaryBankIFSCCode': 'INDU1234567',
    'TransactionAmount': '100.00',
    'Beneficiary Mobile Number': '9876543210',
    'Email ID': 'aaanas372@gmail.com',
    'Reserve1': '',
    'Reserve2': '',
    'Reserve3': '',
}

# This funtion will generate AES-256-bit symmetric key:
key = generate_key()
print("\n\n",key)

#The random AES-256-bit symmetric key will be encrypted with the public certificate 'public_key_pem', followed by the RSA-OAEP-256 algorithm, and will be passed in the key parameter or tag.
public_key = RSA.import_key(public_key_pem)
encrypted_aes_key_with_rsa = encrypt_aes_key_with_rsa(public_key, key)
print("\nEncrypted AES key with rsa:", encrypted_aes_key_with_rsa)

#The AES-256-bit symmetric key will encrypt the data that is going to be passed inside the the request parameters
encrypt_data1= encrypt_data(data, key)
print("\n\n",encrypt_data1)

#This is just a testing and non-usable function just written for debugging, which is used to decrypt the data using AES-256-bit symmetric key.
decrypt_data1 = decrypt_data(encrypt_data1)
print("\n\n",decrypt_data1)

#These are the Request Parameters which will be used for sending Request to API.
payload = {
    "data": encrypt_data1,
    "key": encrypted_aes_key_with_rsa.hex(),
    "bit": 0
}

print("\n\n\n{0}\n\n\n".format(payload))

#API timeout as per the document
api_timeout = 30

#Headers which will be passed along with post request
headers = {
    "IBL-Client-Id": "fce6de82afe45543d10849f5f3f6211c",
    "IBL-Client-Secret": "30777c257ddc85059a7b5cc459ff5f93",
    "Content-Type": "application/json"
}

#function that will be used for sending post request, all the above values of payoad,header, api_timeout will be passed inside it
def send_post_request(payload):
    headers = {
        "IBL-Client-Id": "fce6de82afe45543d10849f5f3f6211c",
        "IBL-Client-Secret": "30777c257ddc85059a7b5cc459ff5f93",
        "Content-Type": "application/json"
    }
    api_url = 'https://indusapiuat.indusind.com/indusapi-np/uat/sync-apis/ISync/ProcessTxn'
    try:
        response = requests.post(api_url, headers=headers,timeout=api_timeout, data=payload)
        response.raise_for_status()  # Raises exception for 4XX and 5XX status codes
        return response.json()  # Assuming response is JSON
    except requests.exceptions.RequestException as e:
        print("\nError:", e)
        return None

response = send_post_request(payload)
if response:
    print("\nResponse:", response)


import secrets
import base64

import requests

def generate_aes_key():
    # Generate 32 bytes (256 bits) of random data
    aes_key = secrets.token_bytes(32)
    # Encode the key using Base64 for storage/transmission
    aes_key_base64 = base64.b64encode(aes_key).decode('utf-8')
    return aes_key_base64

# Example usage:
aes_key = generate_aes_key()
print("Generated AES Key (Base64):", aes_key)

import jwt

# Your payload
payload = {
    'Customerid': '1234567890',
    'Transaction Type': 'DEBIT',
    'CustomerRefNumber': 'REF123',
    'DebitAccountNo': '1234567890123',
    'BeneficiaryName': 'John Doe',
    'CreditAccountNumber': '9876543210987',
    'BeneficiaryBankIFSCCode': 'INDU1234567',
    'TransactionAmount': '100.00',
    'Beneficiary Mobile Number': '9876543210',
    'Email ID': 'vishal.hatiskar@indusind.com',
    'Reserve1': '',
    'Reserve2': '',
    'Reserve3': '',
}

# Secret key for signing the JWT
secret_key = aes_key

# Encode the payload into a JWT
encoded_jwt = jwt.encode(payload, secret_key, algorithm='HS256')

# print("Encoded JWT:", encoded_jwt)


import jwt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.x509 import load_pem_x509_certificate
import base64

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

def encrypt_aes_key_with_certificate(aes_key, public_key_pem):
    # Load the PEM encoded X.509 certificate
    cert = load_pem_x509_certificate(public_key_pem.encode(), default_backend())
    
    # Extract the public key from the certificate
    public_key = cert.public_key()
    
    # Encrypt the AES key using the public key
    encrypted_aes_key = public_key.encrypt(
        aes_key.encode('utf-8'),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    # Convert the encrypted AES key to Base64
    encrypted_aes_key_base64 = base64.b64encode(encrypted_aes_key).decode('utf-8')

    # Encode the encrypted AES key into JWT using HS256 algorithm
    encoded_jwt = jwt.encode({"aes_key": encrypted_aes_key_base64}, aes_key, algorithm='HS256')

    return encoded_jwt

# Example usage:
encrypted_aes_key_jwt = encrypt_aes_key_with_certificate(aes_key, public_key_pem)
# print("Encrypted AES Key JWT:", encrypted_aes_key_jwt)

api_timeout = 30

payload = {
    "data": encoded_jwt,
    "key": encrypted_aes_key_jwt,
    "bit": 0
}

print(payload)

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


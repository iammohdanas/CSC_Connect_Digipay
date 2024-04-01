from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import os

import requests

def generate_aes_key():
    # Generate a random AES-256 bit key
    return os.urandom(32)

def encrypt_payload(payload, key):
    # Convert payload to bytes
    payload_bytes = str(payload).encode('utf-8')

    # Encrypt the payload
    nonce = os.urandom(12)  # Generate a random 96-bit nonce
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(payload_bytes) + encryptor.finalize()

    # Get the tag
    tag = encryptor.tag

    # Encode the ciphertext, tag, and nonce as base64 without padding
    ciphertext_b64 = base64.urlsafe_b64encode(ciphertext).rstrip(b'=').decode('utf-8')
    tag_b64 = base64.urlsafe_b64encode(tag).rstrip(b'=').decode('utf-8')
    nonce_b64 = base64.urlsafe_b64encode(nonce).rstrip(b'=').decode('utf-8')

    # Combine the encoded ciphertext, tag, and nonce
    encrypted_payload = f"{tag_b64}.{nonce_b64}.{ciphertext_b64}"

    return encrypted_payload

def encrypt_key_with_rsa(key, public_key):
    # Load the public key
    rsa_public_key = serialization.load_pem_public_key(public_key, backend=default_backend())

    # Encrypt the key using RSA-OAEP-256 algorithm
    encrypted_key = rsa_public_key.encrypt(
        key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Encode the encrypted key as base64 without padding
    encrypted_key_b64 = base64.urlsafe_b64encode(encrypted_key).rstrip(b'=').decode('utf-8')

    return encrypted_key_b64

# Define the payload
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

# Generate AES key
key = generate_aes_key()

# Encrypt the payload
encrypted_payload = encrypt_payload(payload, key)

# Sample public key


from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.x509 import load_pem_x509_certificate

# Sample certificate
certificate_pem = """-----BEGIN CERTIFICATE-----
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

def extract_public_key_from_certificate(certificate_pem):
    # Load the certificate
    cert = load_pem_x509_certificate(certificate_pem.encode(), default_backend())

    # Extract the public key
    public_key = cert.public_key()

    # Serialize the public key to PEM format
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    return public_key_pem

# Extract the public key from the certificate
public_key = extract_public_key_from_certificate(certificate_pem)

print("Extracted Public Key:")
print(public_key.decode())


# Encrypt the AES key with RSA
encrypted_key = encrypt_key_with_rsa(key, public_key)

# Get the common prefix
common_prefix = encrypted_payload.split('.', 1)[0]

# Construct the request data
request_data = {
    "data": encrypted_payload,
    "key": f"{common_prefix}.{encrypted_key}",
    "bit": 0
}

print("Request data:")
print(request_data)

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

response = send_post_request(request_data)
if response:
    print("\nResponse:", response)
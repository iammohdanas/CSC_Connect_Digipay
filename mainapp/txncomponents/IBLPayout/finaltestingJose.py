import json
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from jose import jwe
from cryptography.x509 import load_pem_x509_certificate
import requests

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
    'Email ID': 'vishal.hatiskar@indusind.com',
    'Reserve1': '',
    'Reserve2': '',
    'Reserve3': '',
}

# Generate a random AES 256-bit symmetric key
def generate_aes_key():
    password = b"random"
    salt = b"salt"
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password)
    return key

random_aes_key = generate_aes_key()
print("\nrandom aes key : {0}\n".format(random_aes_key.hex()))
plaintext = json.dumps(data).encode('utf-8')
# Encrypt payload with the generated key
encrypted_payload = jwe.encrypt(plaintext,key=random_aes_key,algorithm='A256KW', encryption='A256GCM')

print("Encrypted payload:", encrypted_payload)

def decrypt_payload(encrypted_payload, key):
    decrypted_payload = jwe.decrypt(
        encrypted_payload,
        key=key
    )
    return json.loads(decrypted_payload.decode('utf-8'))

# decrypted_payload = decrypt_payload(encrypted_payload, random_aes_key)
# print("Decrypted payload:", decrypted_payload)





# Load your public certificate key
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

# Load the public key from certificate
public_key = load_pem_x509_certificate(public_key_pem.encode(), default_backend()).public_key()


# Encrypt the AES key with RSA-OAEP-256 algorithm
encrypted_key = jwe.encrypt(random_aes_key, public_key, algorithm='RSA-OAEP-256', encryption='A256GCM')

print("Encrypted AES Key:", encrypted_key.decode('utf-8'))


payload = {
    "data": encrypted_payload.decode('utf-8'),
    "key": encrypted_key.decode('utf-8'),
    "bit": 0
}

print("\n\n\n{0}\n\n".format(payload))


api_timeout=30
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

# response = send_post_request(payload)

# if response:
#     print("\nResponse:", response)



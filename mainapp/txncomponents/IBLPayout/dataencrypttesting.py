from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import secrets
import json
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
import requests

def generate_key(length=32):
    # Generate a 32-byte (256-bit) key
    aes_key = secrets.token_bytes(length)
    return aes_key

def pad_data(data):
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data.encode())
    padded_data += padder.finalize()
    return padded_data

def unpad_data(padded_data):
    unpadder = padding.PKCS7(128).unpadder()
    data = unpadder.update(padded_data)
    data += unpadder.finalize()
    return data

def encrypt_data(data, key):
    # Convert data to JSON string
    json_data = json.dumps(data)
    # Pad the data
    padded_data = pad_data(json_data)
    # Generate initialization vector
    iv = secrets.token_bytes(16)
    # Create cipher
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    # Encryptor object
    encryptor = cipher.encryptor()
    # Encrypt the data
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    return iv + encrypted_data

def decrypt_data(encrypted_data, key):
    # Extract initialization vector
    iv = encrypted_data[:16]
    # Extract encrypted data
    encrypted_data = encrypted_data[16:]
    # Create cipher
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    # Decryptor object
    decryptor = cipher.decryptor()
    # Decrypt the data
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()
    # Unpad the decrypted data
    unpadded_data = unpad_data(decrypted_data)
    # Convert JSON string back to dictionary
    decrypted_json = json.loads(unpadded_data.decode())
    return decrypted_json

def encrypt_aes_key_with_rsa(public_key, aes_key):
    # Encrypt AES key using RSA-OAEP
    cipher_rsa = PKCS1_OAEP.new(public_key)
    encrypted_aes_key = cipher_rsa.encrypt(aes_key)
    
    return encrypted_aes_key

# Example usage
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
    'Email ID': 'john.doe@example.com',
    'Reserve1': '',
    'Reserve2': '',
    'Reserve3': '',
}
# Example usage:
key = generate_key()

print("\nAES 256-bit symmetric key:", key)
print("\nAES 256-bit symmetric key:", key.hex())

public_key = RSA.import_key(public_key_pem)

encrypted_aes_key_with_rsa = encrypt_aes_key_with_rsa(public_key, key)
print("\nEncrypted AES key with rsa:", encrypted_aes_key_with_rsa)


encrypted_data = encrypt_data(data, key)
print("\nEncrypted data:", encrypted_data.hex())
decrypted_data = decrypt_data(encrypted_data, key)
print("\nDecrypted data:", decrypted_data)

data = {
    "data": encrypted_data.hex(),
    "key": encrypted_aes_key_with_rsa.hex(),
    "bit": 0
}

print("\n\n\n{0}\n\n\n".format(data))

api_timeout = 30
headers = {
    "IBL-Client-Id": "fce6de82afe45543d10849f5f3f6211c",
    "IBL-Client-Secret": "30777c257ddc85059a7b5cc459ff5f93",
    "Content-Type": "application/json"
}


def send_post_request(data):
    api_url = 'https://indusapiuat.indusind.com/indusapi-np/uat/sync-apis/ISync/ProcessTxn'
    try:
        response = requests.post(api_url, headers=headers, data=data)
        response.raise_for_status()  # Raises exception for 4XX and 5XX status codes
        return response.json()  # Assuming response is JSON
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None
    

# Sending the request
# response = send_post_request(data)
# if response:
#     print("\nResponse:", response)
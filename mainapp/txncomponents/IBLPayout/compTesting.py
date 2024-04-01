import json
import base64
import secrets
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def generate_key(length=32):
    # Generate a 32-byte (256-bit) key
    aes_key = secrets.token_bytes(length)
    return aes_key
key = generate_key(32)

def encrypt_payload(payload):
    # Convert payload to JSON string
    payload_json = json.dumps(payload).encode('utf-8')

    # Generate a random 256-bit AES key


    # Encrypt the payload
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(payload_json)

    # Encode the encrypted data, IV, and tag as base64
    encrypted_data = base64.urlsafe_b64encode(ciphertext).decode('utf-8').rstrip("=")
    iv = base64.urlsafe_b64encode(cipher.nonce).decode('utf-8').rstrip("=")
    tag = base64.urlsafe_b64encode(tag).decode('utf-8').rstrip("=")

    # Create the encrypted payload
    encrypted_payload =  f"{encrypted_data}.{iv}.{tag}"

    return encrypted_payload

# Example payload
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

encrypted_payload = encrypt_payload(payload)


def decrypt_payload(encrypted_payload, key):
    # Extract encrypted data, IV, and tag from the payload
    encrypted_data, iv, tag = encrypted_payload.split(".")
    # Add padding '=' characters to encoded strings if needed
    encrypted_data += '=' * (-len(encrypted_data) % 4)
    iv += '=' * (-len(iv) % 4)
    tag += '=' * (-len(tag) % 4)
    # Decode base64 strings
    encrypted_data = base64.urlsafe_b64decode(encrypted_data)
    iv = base64.urlsafe_b64decode(iv)
    tag = base64.urlsafe_b64decode(tag)
    # Create cipher object
    cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
    # Decrypt and verify the payload
    decrypted_data = cipher.decrypt_and_verify(encrypted_data, tag)
    # Convert decrypted JSON string back to Python object
    decrypted_payload = json.loads(decrypted_data.decode('utf-8'))
    return decrypted_payload


import os
import json
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA

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

pu1 = RSA.import_key(public_key_pem)
print(pu1)

def encrypt_aes_key_with_rsa(aes_key, public_key_pem):
    public_key = RSA.import_key(public_key_pem)
    cipher_rsa = PKCS1_OAEP.new(public_key)
    encrypted_key = cipher_rsa.encrypt(aes_key)
    return encrypted_key


# Encrypt AES key using RSA-OAEP-256 with public key
# Update with your public key file
encrypted_aes_key = encrypt_aes_key_with_rsa(key, public_key_pem)
print(encrypted_aes_key.hex())

# Create JSON output
output_data = {
    "data": encrypted_payload,
    "key": encrypted_aes_key.hex()
}
print(json.dumps(output_data, indent=4))

print("decrypted payload : ",decrypt_payload(encrypted_payload, key))
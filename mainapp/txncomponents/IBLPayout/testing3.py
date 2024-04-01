import os
import secrets
from jose import jwe
import json

def generate_aes_key():
    key = os.urandom(32) # 256-bit key
    return key

# Function to convert bytes to hex
def bytes_to_hex(bytestring):
    return bytestring.hex()

# Generate AES key
key = generate_aes_key()

# Convert key to hex
encoded_key = bytes_to_hex(key)

print("Encoded key:", encoded_key)

# Your payload dictionary
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

# Convert payload dictionary to JSON string
payload_json = json.dumps(payload)

# Convert payload JSON string to bytes
payload_bytes = payload_json.encode('utf-8')

# Create JWE object
jwe_object = jwe.encrypt(
    payload_bytes,
    key,  # Use the AES key directly for encryption
    algorithm='dir',  # Use 'dir' algorithm since we're using a direct symmetric key
    encryption='A256GCM',  # Encryption method
)

# Serialize JWE object
encrypted_payload = jwe_object

print("Encrypted Payload:", encrypted_payload)

from jose import jwk, jwe
import json
import base64

# Convert payload dictionary to JSON string
payload_json = json.dumps(payload)

# Generate a random symmetric key
key = jwk.generate_key('oct', size=256)

# Encrypt the payload using A256KW algorithm
encrypted = jwe.encrypt(
    payload_json.encode('utf-8'),
    key,
)

# Base64 encode the encrypted payload
encrypted_base64 = base64.urlsafe_b64encode(encrypted)

print("Encrypted payload:", encrypted_base64.decode())
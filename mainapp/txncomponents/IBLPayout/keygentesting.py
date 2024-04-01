import secrets
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP

# def generate_aes_key():
#     # Generate a 32-byte (256-bit) key
#     aes_key = secrets.token_bytes(32)
#     return aes_key

def generate_key(length=32):
    # Generate a 32-byte (256-bit) key
    aes_key = secrets.token_bytes(length)
    return aes_key

# Example usage
aes_key = generate_key(32)
print("AES 256-bit symmetric key:", aes_key)

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
public_key = RSA.import_key(public_key_pem)

encrypted_aes_key = encrypt_aes_key_with_rsa(public_key, aes_key)
print("\nEncrypted AES key:", encrypted_aes_key)



import requests

def send_post_request(data):
    headers = {
        "IBL-Client-Id": "fce6de82afe45543d10849f5f3f6211c",
        "IBL-Client-Secret": "30777c257ddc85059a7b5cc459ff5f93",
        "Content-Type": "application/json"
    }

    api_url = 'https://indusapiuat.indusind.com/indusapi-np/uat/sync-apis/ISync/ProcessTxn'

    try:
        response = requests.post(api_url, headers=headers, data=data)
        response.raise_for_status()  # Raises exception for 4XX and 5XX status codes
        return response.json()  # Assuming response is JSON
    except requests.exceptions.RequestException as e:
        print("\nError:", e)
        return None

# Example data
data = {
    "data": "kSzhT461mIuEzI7fxK8ZjlLGIZkWgKiKsWIRQ6cFyZ2IKTcIwO6VQl/l9goSHPS7loq6oabH6wq2JmWAUa7lSI95U7U0omzYmq94XB9Z65zJgpELAeaS9+Tx/UB1G/uYto5pmz6UZ71IBnWv2hVFfqniEaQ7cC970wLYYGzPFAu+R3c27IvUJ6r/cIO85r7DoezUE6xr7FM3hnNd1xhMRVKfyI0X25T7wjwBWwIojOrdeY0r73/8i7sIxJyaXDS63AANZhmT88LsfwKchm56QmPYdG2nMUkesUXLiGa+R+o2g4TxJjRmGXvmTqlI6oGAYUsvhS8bIAPat+1zgZCH91rojvJY/kY990B9er2R/JHyUOgjhzgEKJgce8bSNr4rOTKHii31V2eExvS7WzCHmZs0dlTbKzFnZlXPdl5eidW3WYzh2RzQDqmkcQBMb3EQawKNt1y4/GTrwpj0JEli8XIUpNX+9kBaXPN+tTkoXDkMU4tHHT1j8sryHosMA/DznM38+IEK/hGwrizsvjqLxBDpCPWU4fhNEImGh24uG2k=",
    "key": encrypted_aes_key,
    "bit": 0
}

# Sending the request
response = send_post_request(data)
if response:
    print("\nResponse:", response)

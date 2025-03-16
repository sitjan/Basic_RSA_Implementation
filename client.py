import requests
import os
import rsa

# Disable proxy for localhost
os.environ['NO_PROXY'] = '127.0.0.1'

# Fetch public key from server
response = requests.get('http://127.0.0.1:5000/getkey')
public_key_raw = response.content.decode('ascii').strip()[1:-1]  # Clean up key format
public_key = rsa.PublicKey.load_pkcs1(public_key_raw)

# Loop to send encrypted messages
while True:
    user_input = input("Enter message (or type 'exit' to quit):\n")
    if user_input.lower() == 'exit':
        print("Exiting...")
        break

    # Encrypt the message using the server's public key
    encrypted_msg = rsa.encrypt(user_input.encode(), public_key)
    print(f"Encrypted Message Sent: {encrypted_msg}\n")

    # Send the encrypted message to the server
    server_response = requests.post('http://127.0.0.1:5000/message', data=encrypted_msg)
    print(f"Server Response: {server_response.content.decode()}\n")
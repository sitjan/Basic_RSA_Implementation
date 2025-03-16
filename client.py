import requests
import os
import rsa
import json

# Disable proxy for localhost
os.environ['NO_PROXY'] = '127.0.0.1'

# Fetch public key from server
try:
    response = requests.get('http://127.0.0.1:8080/getkey')  # Changed port to 8080 to match server
    
    # Parse the jsonpickle response correctly
    decoded_response = json.loads(response.content)
    public_key_raw = decoded_response
    
    # Load the public key properly
    public_key = rsa.PublicKey.load_pkcs1(public_key_raw)
    print("Successfully loaded the public key from server")
    
except Exception as e:
    print(f"Error fetching or parsing the public key: {e}")
    exit(1)

# Loop to send encrypted messages
while True:
    try:
        user_input = input("Enter message (or type 'exit' to quit):\n")
        if user_input.lower() == 'exit':
            print("Exiting...")
            break
            
        # Encrypt the message using the server's public key
        encrypted_msg = rsa.encrypt(user_input.encode('utf-8'), public_key)
        print(f"Message encrypted successfully")
        
        # Send the encrypted message to the server
        server_response = requests.post('http://127.0.0.1:8080/message', data=encrypted_msg)
        
        # Handle the server response
        if server_response.status_code == 200:
            print(f"Server Response: {server_response.content.decode()}\n")
        else:
            print(f"Error: Server returned status code {server_response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")
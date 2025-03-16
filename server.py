from flask import Flask, request
import rsa
import jsonpickle
import os

app = Flask(__name__)

# Generate RSA keys when server starts
def generate_keys_if_needed():
    try:
        with open("private.pem", "r") as private_file:
            with open("public.pem", "r") as public_file:
                print("Keys already exist.")
                return
    except FileNotFoundError:
        print("Generating new keys...")
        publicKey, privateKey = rsa.newkeys(2048)
        publicKey_PEM = publicKey.save_pkcs1().decode('utf8')
        privateKey_PEM = privateKey.save_pkcs1().decode('utf8')
        
        with open("private.pem", "w") as private_file:
            private_file.write(privateKey_PEM)
        
        with open("public.pem", "w") as public_file:
            public_file.write(publicKey_PEM)
        
        print("Keys generated successfully.")

# Generate keys at startup
generate_keys_if_needed()

@app.route("/")
def home():
    return "<p>OK!</p>"

# Serve the public key
@app.route("/getkey")
def serve_public_key():
    with open("public.pem", "r") as public_file:
        response = public_file.read()
    return jsonpickle.encode(response)  # Return as json format

# Decrypt and process incoming messages
@app.route("/message", methods=['POST'])
def process_message():
    with open("private.pem", "r") as private_file:
        private_key = rsa.PrivateKey.load_pkcs1(private_file.read())
    
    encrypted_data = request.data
    print(encrypted_data)
    decrypted_message = rsa.decrypt(encrypted_data, private_key).decode()
    print(f"Decrypted Message: {decrypted_message}")
    return "Message received by server"

# Test endpoint for debugging
@app.route("/test", methods=['POST'])
def test_endpoint():
    with open("private.pem", "r") as private_file:
        private_key = rsa.PrivateKey.load_pkcs1(private_file.read())
    
    encrypted_data = request.data
    print(encrypted_data)
    decrypted_message = rsa.decrypt(encrypted_data, private_key).decode()
    print(f"Test Decryption: {decrypted_message}")
    return decrypted_message

if __name__ == "__main__":
    app.run(debug=True, port=8080, use_reloader=False)
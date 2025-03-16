from flask import Flask, request
import rsa

app = Flask(__name__)

# Generate RSA keys if they don't exist
def generate_keys():
    try:
        with open("private.pem", "r") as private_file, open("public.pem", "r") as public_file:
            return "<p>Status OK!</p>"
    except FileNotFoundError:
        public_key, private_key = rsa.newkeys(2048)
        with open("private.pem", "w") as private_file, open("public.pem", "w") as public_file:
            private_file.write(private_key.save_pkcs1().decode())
            public_file.write(public_key.save_pkcs1().decode())
        return "<p>Keys Generated!</p>"

# Serve the public key
@app.route("/getkey")
def serve_public_key():
    with open("public.pem", "r") as public_file:
        return public_file.read()

# Decrypt and process incoming messages
@app.route("/message", methods=['POST'])
def process_message():
    with open("private.pem", "r") as private_file:
        private_key = rsa.PrivateKey.load_pkcs1(private_file.read())
    encrypted_data = request.data
    decrypted_message = rsa.decrypt(encrypted_data, private_key).decode()
    print(f"Decrypted Message: {decrypted_message}")
    return "Message received by server"

# Test endpoint for debugging
@app.route("/test", methods=['POST'])
def test_endpoint():
    with open("private.pem", "r") as private_file:
        private_key = rsa.PrivateKey.load_pkcs1(private_file.read())
    encrypted_data = request.data
    decrypted_message = rsa.decrypt(encrypted_data, private_key).decode()
    print(f"Test Decryption: {decrypted_message}")
    return decrypted_message

if __name__ == "__main__":
    app.run(debug=True, port=8080, use_reloader=False)
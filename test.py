import requests
import os
import rsa
import unittest

class TestEncryption(unittest.TestCase):
    def test_decryption(self):
        # Disable proxy for localhost
        os.environ['NO_PROXY'] = '127.0.0.1'

        # Fetch and load the server's public key
        response = requests.get('http://127.0.0.1:5000/getkey')
        public_key_raw = response.content.decode('ascii').strip()[1:-1]
        public_key = rsa.PublicKey.load_pkcs1(public_key_raw)

        # Define and encrypt a test message
        test_message = "Test message. Anyone there?"
        encrypted_message = rsa.encrypt(test_message.encode(), public_key)

        # Send the encrypted message to the test endpoint
        server_response = requests.post('http://127.0.0.1:5000/test', data=encrypted_message)
        decrypted_response = server_response.content.decode()

        # Assert that the decrypted message matches the original
        self.assertEqual(test_message, decrypted_response)

if __name__ == '__main__':
    unittest.main()
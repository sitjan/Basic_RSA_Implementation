import requests
import os
import rsa
import unittest
import json

class TestEncryption(unittest.TestCase):
    def test_decryption(self):
        # Disable proxy for localhost
        os.environ['NO_PROXY'] = '127.0.0.1'
        try:
            # Fetch and load the server's public key
            response = requests.get('http://127.0.0.1:8080/getkey')  # Updated port to 8080
            response.raise_for_status()  # Raise an exception for HTTP errors
            
            # Properly decode the jsonpickle response
            decoded_response = json.loads(response.content)
            public_key_raw = decoded_response
            
            # Load the public key
            public_key = rsa.PublicKey.load_pkcs1(public_key_raw)
            print("Successfully loaded the public key")
            
            # Define and encrypt a test message
            test_message = "Test message. Anyone there?"
            encrypted_message = rsa.encrypt(test_message.encode('utf-8'), public_key)
            print(f"Message encrypted successfully")
            
            # Send the encrypted message to the test endpoint
            server_response = requests.post('http://127.0.0.1:8080/test', data=encrypted_message)  # Updated port
            server_response.raise_for_status()  # Raise an exception for HTTP errors
            
            # Decode the server's response
            decrypted_response = server_response.content.decode()
            print(f"Response received: {decrypted_response}")
            
            # Assert that the decrypted message matches the original
            self.assertEqual(test_message, decrypted_response)
            print("Test passed: Original and decrypted messages match")
            
        except requests.exceptions.RequestException as e:
            self.fail(f"HTTP request failed: {e}")
        except rsa.pkcs1.VerificationError as e:
            self.fail(f"Decryption failed: {e}")
        except Exception as e:
            self.fail(f"An unexpected error occurred: {e}")
            
if __name__ == '__main__':
    unittest.main()
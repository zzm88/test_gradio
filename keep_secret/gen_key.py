import hashlib
import base64
from cryptography.fernet import Fernet
import os
from gen_hardware_id import generate_hardware_identifier

hardware_id = generate_hardware_identifier()

def generate_key_with_hardware_identifier(hardware_identifier):
    combined_data = hardware_identifier.encode()
    key = hashlib.sha256(combined_data).digest()
    fernet_key = base64.urlsafe_b64encode(key)
    return fernet_key

path = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':

    # Generate a new encryption key
    encryption_key = generate_key_with_hardware_identifier(hardware_id)

    # Save the encryption key to a file or securely store it
    with open(path+'/encryption_key.key', 'wb') as key_file:
        print(encryption_key)
        key_file.write(encryption_key)

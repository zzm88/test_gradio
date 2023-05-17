import base64
import hashlib
import os
import platform
from cryptography.fernet import Fernet
from keep_secret import gen_hardware_id  

key_file_path = os.path.dirname(os.path.abspath(__file__)) + '/encryption_key.key'

def retrieve_key_with_hardware_identifier(hardware_identifier):
    with open(key_file_path, 'rb') as key_file:
        key = key_file.read()

    combined_data = hardware_identifier.encode()
    expected_key = hashlib.sha256(combined_data).digest()
    # Convert the binary digest to a URL-safe base64-encoded string
    expected_key = base64.urlsafe_b64encode(expected_key)

    if key == expected_key:
        return key
    else:
        raise ValueError("Unauthorized access. Hardware identifier mismatch.")

def decrypt_file(encrypted_file_path, hardware_identifier):
    with open(encrypted_file_path, 'rb') as file:
        encrypted_data = file.read()

    encryption_key = retrieve_key_with_hardware_identifier(hardware_identifier)

    fernet = Fernet(encryption_key.decode())  # Decode the encryption key
    decrypted_data = fernet.decrypt(encrypted_data)

    # Now compare the original and decrypted files
    original_file_path = working_dir + '/panda1_v1.safetensors'
    original_file = open(original_file_path, 'rb')
    original_data = original_file.read()

    if are_files_identical(original_data, decrypted_data):
        print("The original and decrypted files are YES identical.")
        #save decrypted_data to file called "panda1_v1_decrypted.safetensors"
    else:
        print("The original and decrypted files are NOT identical.")

    #do something with decrypted_data later
    pass
    # return decrypted_data


def are_files_identical(data1, data2):

    return data1 == data2



if __name__ == '__main__':
    working_dir = os.path.dirname(os.path.abspath(__file__))
    pth_file = working_dir + '/panda1_v1.safetensors.encrypted'
    encrypted_file_path = pth_file

    hardware_identifier = gen_hardware_id.generate_hardware_identifier()

    decrypt_file(encrypted_file_path, hardware_identifier)
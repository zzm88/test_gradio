# -*- coding: utf-8 -*-
from cryptography.fernet import Fernet
import os

#read currentdir + encryption_key.key
key_file_path = os.path.dirname(os.path.abspath(__file__)) + '/encryption_key.key'



working_dir = os.path.dirname(os.path.abspath(__file__))
pth_file = working_dir + '/panda1_v1.safetensors'

def encrypt_file(file_path, encryption_key):
    with open(file_path, 'rb') as file:
        plaintext = file.read()

    fernet = Fernet(encryption_key)
    encrypted_data = fernet.encrypt(plaintext)

    encrypted_file_path = file_path + '.encrypted'
    with open(encrypted_file_path, 'wb') as file:
        file.write(encrypted_data)
    
    print("File encrypted successfully.")

def get_key(key_file_path):
    with open(key_file_path, 'rb') as key_file:
        key = key_file.read()
    return key

# Provide the path to your .pth file and the encryption key
if __name__ == '__main__':
    key = get_key(key_file_path)
    encrypt_file(pth_file, key)
    
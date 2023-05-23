import os
import sys
from cryptography.fernet import Fernet
import uuid
import random

# Specify the path to the folder where you want to store keys and the encrypted MAC address
folder_path = '/workdirectory/key/'  # changed directory path

def get_mac_address():
    mac_num = hex(uuid.getnode()).replace('0x', '').upper()
    mac = '-'.join(mac_num[i: i + 2] for i in range(0, 11, 2))
    return mac

def write_key():
    key = Fernet.generate_key()
    with open(os.path.join(folder_path, "key.key"), "wb") as key_file:
        key_file.write(key)

def load_key():
    return open(os.path.join(folder_path, "key.key"), "rb").read()

def encrypt_mac_address(mac_address):
    key = load_key()
    f = Fernet(key)
    mac_address = mac_address.encode()
    encrypted = f.encrypt(mac_address)
    with open(os.path.join(folder_path, "mac_address.key"), "wb") as key_file:
        key_file.write(encrypted)

def decrypt_mac_address():
    key = load_key()
    f = Fernet(key)
    with open(os.path.join(folder_path, "mac_address.key"), "rb") as key_file:
        encrypted_mac_address = key_file.read()
    decrypted_mac_address = f.decrypt(encrypted_mac_address).decode()
    return decrypted_mac_address

def gen_unvalid_mac_secret():
    # Generate an invalid MAC address
    unvalid_mac = ":".join(["{:02x}".format(random.randint(0, 255)) for _ in range(6)])

    # Encrypt and save the invalid MAC address
    encrypt_mac_address(unvalid_mac)

if __name__ == "__main__":
    mac_file_path = os.path.join(folder_path, "mac_address.key")
    if os.path.isfile(mac_file_path):
        decrypted_mac_address = decrypt_mac_address()
        current_mac_address = get_mac_address()
        if decrypted_mac_address != current_mac_address:
            print('MAC addresses do not match!')
            # call your comparison function here, if any
    else:
        if len(sys.argv) > 1 and sys.argv[1] == 'gen_wrong_mac':
            gen_unvalid_mac_secret()
            print('生成一个无效key')
        else:
            write_key()
            encrypt_mac_address(get_mac_address())
            print('生成一个有效key')

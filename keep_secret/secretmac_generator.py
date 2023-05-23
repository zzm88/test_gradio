import uuid
import os
from cryptography.fernet import Fernet
import sys
import random

# Specify the path to the folder where you want to store keys and the encrypted MAC address
folder_path = '/Users/ming/Documents/GitHub/stable-diffusion-webui/keep_secret/'  # current directory

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
    with open(os.path.join(folder_path, "./mac_address.key"), "wb") as key_file:
        key_file.write(encrypted)

def gen_unvalid_mac_secret():
    # Generate an invalid MAC address
    unvalid_mac = ":".join(["{:02x}".format(random.randint(0, 255)) for _ in range(6)])

    # Encrypt and save the invalid MAC address
    encrypt_mac_address(unvalid_mac)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'gen_wrong_mac':
        gen_unvalid_mac_secret()
        print('生成一个无效key')
    else:
        write_key()
        encrypt_mac_address(get_mac_address())
        print('生成一个有效key')
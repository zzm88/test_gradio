import uuid
import os
from cryptography.fernet import Fernet

# Specify the path to the folder where you stored keys and the encrypted MAC address
folder_path = 'keep_secret'  # current directory

def get_mac_address():
    mac_num = hex(uuid.getnode()).replace('0x', '').upper()
    mac = '-'.join(mac_num[i: i + 2] for i in range(0, 11, 2))
    return mac

def load_key():
    return open(os.path.join(folder_path, "key.key"), "rb").read()

def decrypt_mac_address():
    key = load_key()
    f = Fernet(key)
    with open(os.path.join(folder_path, "mac_address.key"), "rb") as key_file:
        encrypted = key_file.read()
    decrypted = f.decrypt(encrypted)
    return decrypted.decode()

def verify_mac_address():
    actual_mac = get_mac_address()
    decrypted_mac = decrypt_mac_address()

    if actual_mac == decrypted_mac:
        return True
    else:
        return False

actual_mac = get_mac_address()
decrypted_mac = decrypt_mac_address()

# if actual_mac == decrypted_mac:
#     print('MAC addresses match. Continue with the script...')
#     # Continue with the rest of your script here
# else:
#     print('MAC addresses do not match. Exiting...')
#     exit()


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
    try:
        return open(os.path.join(folder_path, "key.key"), "rb").read()
    except FileNotFoundError:
        #write key
        write_key()

def write_key():
    key = Fernet.generate_key()
    with open(os.path.join(folder_path, "key.key"), "wb") as key_file:
        key_file.write(key)

def decrypt_mac_address():
    key = load_key()
    f = Fernet(key)
    try:
        with open(os.path.join(folder_path, "mac_address.key"), "rb") as key_file:
            encrypted = key_file.read()
    except FileNotFoundError:
        print("首次执行")
        #ask for password in prompt
        psw = input("请输入管理员密码:")
        if psw == "eeff":
            print("密码正确")
        else:
            print("密码错误,请联系管理员")
            exit()
         
        encrypt_mac_address(get_mac_address())
        with open(os.path.join(folder_path, "mac_address.key"), "rb") as key_file:
            encrypted = key_file.read() 
  
    decrypted = f.decrypt(encrypted)
    return decrypted.decode()


def encrypt_mac_address(mac_address):
    key = load_key()
    f = Fernet(key)
    mac_address = mac_address.encode()
    encrypted = f.encrypt(mac_address)
    with open(os.path.join(folder_path, "./mac_address.key"), "wb") as key_file:
        key_file.write(encrypted)


def verify_mac_address():
    actual_mac = get_mac_address()
    decrypted_mac = decrypt_mac_address()

    if actual_mac == decrypted_mac:
        return True
    else:
        return False

actual_mac = get_mac_address()
decrypted_mac = decrypt_mac_address()




        

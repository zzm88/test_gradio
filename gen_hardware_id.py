import hashlib
from cryptography.fernet import Fernet
import platform
import os

def generate_hardware_identifier():
    cpu_id = hashlib.sha256(platform.processor().encode()).hexdigest()
    motherboard_serial = hashlib.sha256(platform.node().encode()).hexdigest()
    network_card_mac = hashlib.sha256(':'.join(hex(i)[2:].zfill(2) for i in hashlib.md5(platform.node().encode()).digest()).encode()).hexdigest()

    hardware_identifier = cpu_id + motherboard_serial + network_card_mac
    print(hardware_identifier)
    return hardware_identifier


# if main
if __name__ == '__main__':
    generate_hardware_identifier()
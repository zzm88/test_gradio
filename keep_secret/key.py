import uuid

def get_mac():
    mac_address = uuid.getnode()
    mac = ':'.join(("%012X" % mac_address)[i:i + 2] for i in range(0, 12, 2))
    return mac

def check_mac():
    expected_mac = '92:41:E9:D3:CB:3'

    actual_mac = get_mac()
    if actual_mac == expected_mac:
        print('认证成功')
        return True
    else:
        print('认证失败, 请联系管理员')
        return False

if __name__ == '__main__':
    if not check_mac():
        print("请联系管理员")
        exit(0)
    else:
        pass
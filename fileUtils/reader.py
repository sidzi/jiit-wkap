from encryptionUtils import decryption


def read():
    target = open("user.conf", 'r')
    try:
        memcode = target.readline()
        passcode = target.readline()
        if memcode is '' or passcode is '':
            return None, None
    except FileNotFoundError:
        return None, None
    return memcode, passcode

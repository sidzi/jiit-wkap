def read():
    try:
        target = open("user.conf", 'r')
    except IOError:
        return None, None
    memcode = target.readline()
    passcode = target.readline()

    if not memcode or not passcode:
        return None, None

    return memcode[:-1], passcode[:-1]

def read():
    try:
        target = open("user.conf", 'r')
    except IOError:
        return None, None
    memcode = target.readline()[:-1]
    passcode = target.readline()[:-1]

    if memcode is '' or passcode is '':
        return None, None

    return memcode, passcode

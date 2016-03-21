def write(memcode, passcode):
    target = open("user.conf", 'w')
    target.truncate()
    target.write(memcode)
    target.write("\n")
    target.write(passcode)
    target.write("\n")
    target.close()

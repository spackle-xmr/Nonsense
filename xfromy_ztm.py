def xfrompoint_ztm(pointcheck): #Function receives Point, calculates x coordinate via 2.4.2
    ypbytes=bytearray.fromhex(repr(pointcheck))
    biny = bin(int.from_bytes(ypbytes, "little"))[2:].zfill(256)
    b = biny[0]
    newbin = biny[1:]
    newy = '0' + newbin
    y = int(newy,2)
    xp = 0

    u = (y*y - 1) % q 
    v = (d*y*y + 1) % q
    z = (u * v**3) * pow(u*v**7,((q-5)//8), q) % q

    if ((v*z**2) % q) == (u % q):
        xp = (z % q)
    if ((v*z**2) % q) == (-u % q):
        xp = z * pow(2,((q-1)//4), q) % q
    
    if b != bin(xp)[-1]:
        return -xp % q
    else:
        return xp % q


def xfromy_ztm(yp): #Function receives integer y value, calculates x coordinate via 2.4.2
    biny = bin(yp)[2:].zfill(256)
    b = biny[0]
    newbin = biny[1:]
    newy = '0' + newbin
    y = int(newy,2)
    xp = 0

    u = (y*y - 1) % q 
    v = (d*y*y + 1) % q
    z = (u * v**3) * pow(u*v**7,((q-5)//8), q) % q

    if ((v*z**2) % q) == (u % q):
        xp = (z % q)
    if ((v*z**2) % q) == (-u % q):
        xp = z * pow(2,((q-1)//4), q) % q

    print(b)
    print(bin(xp)[-1])
    
    if b != bin(xp)[-1]:
        return -xp % q
    else:
        return xp % q


#match xfromy
def xfromy_ztm(yin):

    #biny = bin(yin)[2:].zfill(260) #weird experiment
    biny = bin(yin)[2:].zfill(255)
    b = biny[0]
    newbin = biny[1:]
    newy = '0' + newbin
    #y = int(newy,2)
    y=yin #passing yprime to decoding process seemingly gives correct answer w/modified logic.
    xp = 0

    u = (y*y - 1) % q 
    v = (d*y*y + 1) % q
    z = (u * v**3) * pow(u*v**7,((q-5)//8), q) % q

    if ((v*z**2) % q) == (u % q):
        xp = (z % q)
    if ((v*z**2) % q) == (-u % q):
        xp = z * pow(2,((q-1)//4), q) % q

    print('b=',b)
    print('xp_bit=',bin(xp)[-1])

    #if b != bin(xp)[-1]:
    if bin(xp)[-1] == '1':
        return -xp % q
    else:
        return xp % q

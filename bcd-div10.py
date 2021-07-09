
DIGITS="0123456789"

def bcd8(n,sz=8):
    c=0
    h=1<<(sz-1)
    while sz:
        if (c&0x0f) >= 0x05: c+=0x03
        if (c&0xf0) >= 0x50: c+=0x30
        c<<=1
        if n&h:
            c|=1
        n<<=1
        sz-=1
    return c

def divmod10(n,sz):
    c=0
    h=1<<(sz-1)
    while sz:
        if (c&0x0f) >= 0x05: c+=0x03
        c<<=1
        if n&h: c|=1
        n<<=1
        sz-=1
    return c>>4,c&0xf

def numprint(n,sz=16):
    if n<10: r=n
    else:
        n,r=divmod10(n,sz)
        numstr(n,sz)
    print(DIGITS[r],end='')

def numstr(n,sz=16):
    if n<10: return DIGITS[n]
    else:
        n,r=divmod10(n,sz)
        v=numstr(n,sz-3) # reduce precision by 3 bits, 
        return v+DIGITS[r]

def numstr_iter(n,sz=16):
    p=""
    while n>=10:
        n,r=divmod10(n,sz)
        sz-=3
        p=p+DIGITS[r]
    p+=DIGITS[n]
    return p[::-1] # reverse
        
#n=bcd8(0x19)
n=bcd8(65535,16)
print("{:x}".format(n))
#numprint(123456789,32)
#print(numstr(0,32))
#print(numstr(1,32))
#print(numstr(5,32))
#print(numstr(9,32))
#print(numstr(10,32))
#print(numstr(11,32))
#print(numstr(123456789,32))
print(numstr_iter(12345678,32))

#MIN_RANGE=radix
#MAX_RANGE=radix*256
SHIFT=8
MASK=0xFFFF
HMSK=0xFF00
class coder_context:
    def __init__(self,vin,radix=256):
        self.r=1 # code is l/r
        self.l=0
        self.v=vin
        self.radix=radix # also min.range
        self.max=radix*radix
        self.buf=256 # for encoder
        self.cnt=0 # carry count
        self.cnt_rr=0
        self.cnt_rw=0
        
def renorm_and_read(dc):
    dc.cnt_rr+=1
    dc.r*=dc.radix
    dc.l*=dc.radix
    if len(dc.v)>0: dc.l+=dc.v.pop(0)

def write_and_carry(dc,x,n):
    def put(x):
        dc.v.append(x)
    if dc.buf!=256: put(dc.buf&0xFF)
    for _ in range(dc.cnt-1):put(x)
    dc.cnt=0
    dc.buf=n

def renorm_and_write(dc):
    dc.cnt_rw+=1
    if dc.l>=dc.max:
        dc.buf+=1
        dc.l&=MASK
        if dc.cnt>0:
            dc.cnt-=1
            write_and_carry(dc,0,256)
            dc.buf=256
    while dc.r<dc.radix:
        if dc.l<(0xFF<<SHIFT):
            write_and_carry(dc,0xFF,dc.l>>SHIFT)
        else:
            dc.cnt+=1
        dc.l<<=8
        dc.l&=MASK
        dc.r<<=8

def encode_finish(dc):
    if dc.l>=dc.max:
        dc.buf+=1
        dc.l&=MASK
        c=0
    else: c=0xFF
    write_and_carry(dc,c,256)
    q=MASK
    l=dc.l
    while q and l:
        dc.v.append(l>>SHIFT)
        l<<=8
        l&=MASK
        q>>=8

def renorm_freq(ct):
    if ct[0]+ct[1]>63-2:
        ct[0]//=2
        ct[1]//=2

def dec_bit(dc,ct):
    if dc.r<dc.radix:
        renorm_and_read(dc)
    ft=ct[0]+ct[1]+2
    spl=dc.r*(ct[0]+1)//ft
    b=1 if dc.l>=spl else 0
    if b:
        dc.l-=spl
        dc.r-=spl
    else:
        dc.r=spl
    return b

def enc_bit(dc,ct,b):
    ft=ct[0]+ct[1]+2
    spl=dc.r*(ct[0]+1)//ft
    if b:
        dc.l+=spl
        dc.r-=spl
    else:
        dc.r=spl
    renorm_and_write(dc)

    
def encode(bs,sz=64):
    dc=coder_context([])
    dc.r=dc.max
    ct=[0,0]
    bq=1<<(sz-1)
    while bq:
        b=1 if bq&bs else 0
        enc_bit(dc,ct,b)
        ct[b]+=1
        renorm_freq(ct)
        bq>>=1
    encode_finish(dc)
    return dc.v

def decode(v,sz=64):
    dc=coder_context(v)
    ct=[0,0]
    bq=1<<(sz-1)
    bo=0
    renorm_and_read(dc) # two radix, fill to mask
    renorm_and_read(dc)
    while bq:
        b=dec_bit(dc,ct)
        ct[b]+=1
        renorm_freq(ct)
        if b:bo|=bq
        bq>>=1
    return bo

def PB(x): return "{:08b}".format(x)
def pall(x):
    for k in x:
        print(PB(k),end=' ')
    print()

def test_encdec():
    bi=0b1010101010000000000000000000000010000000000000000000000000000001
    sz=64
    print("inb","{:08b}".format(bi))
    v=encode(bi,sz)
    print("cod",end=' ')
    pall(v)
    b=decode(v,sz)
    print("out","{:08b}".format(b))


def test_diff():
    sx='%'
    cx=chr_data(sx)
    e1=cx
    #e1=diff_v(e1)
    #e1=diff_h(e1)
    #e1=diff_v(e1)
    prdata(e1)
    cbx=data2bits(cx)
    print("{:64b}".format(cbx))
    v=encode(cbx,64)
    pall(v)

from ac0 import *

if __name__ == "__main__":
    #test_binload()
    #test_diff()
    test_encdec()


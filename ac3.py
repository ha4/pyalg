#MIN_RANGE=radix
#MAX_RANGE=radix*256
SHIFT=8
class coder_context:
    def __init__(self,vin,radix=256):
        self.r=1 # code is l/r
        self.l=0
        self.v=vin
        self.radix=radix # also min.range
        self.max=radix*radix
        self.buf=256 # for encoder
        self.cnt=0 # 0xFF carry count
        self.cnt_rr=0
        self.cnt_rw=0
        
def renorm_and_read(dc):
    dc.cnt_rr+=1
    dc.r*=dc.radix
    dc.l*=dc.radix
    if len(dc.v)>0: dc.l+=dc.v.pop(0)

def write_and_carry(dc,x,buf):
    def put(x):
        dc.v.append(x)
    if dc.buf!=256: put(dc.buf&0xFF)
    for _ in range(dc.cnt):put(x)
    dc.cnt=0
    dc.buf=buf

def renorm_and_write(dc):
    dc.cnt_rw+=1
    if dc.l>=dc.max:
        dc.buf+=1
        dc.l&=dc.max-1
        if dc.cnt>0:
            dc.cnt-=1
            write_and_carry(dc,0x00,256)
    while dc.r<dc.radix:
        x=dc.l>>SHIFT
        if x==0xFF: dc.cnt+=1
        else: write_and_carry(dc,0xFF,x)
        dc.l<<=8
        dc.l&=dc.max-1
        dc.r<<=8

def encode_finish(dc):
    if dc.l>=dc.max:
        dc.buf+=1
        dc.l&=dc.max-1
        c=0x00
    else: c=0xFF
    write_and_carry(dc,c,256)
    q=dc.max-1
    l=dc.l
    while q and l:
        dc.v.append(l>>SHIFT)
        l<<=8
        l&=dc.max-1
        q>>=8

def renorm_freq(ct):
    if ct[0]+ct[1]>63-2:
        if ct[0]>1: ct[0]//=2
        if ct[1]>1: ct[1]//=2

def dec_bit(dc,ct):
    if dc.r<dc.radix:
        renorm_and_read(dc)
    ft=ct[0]+ct[1]
    spl=dc.r*ct[0]//ft
    b=1 if dc.l>=spl else 0
    if b:
        dc.l-=spl
        dc.r-=spl
    else:
        dc.r=spl
    return b

def enc_bit(dc,ct,b):
    renorm_and_write(dc)
    ft=ct[0]+ct[1]
    spl=dc.r*ct[0]//ft
    if b:
        dc.l+=spl
        dc.r-=spl
    else:
        dc.r=spl

    
def encode_bits(bs,sz=64):
    dc=coder_context([])
    dc.r=dc.max
    ct=[1,1]
    bq=1<<(sz-1)
    while bq:
        b=1 if bq&bs else 0
        enc_bit(dc,ct,b)
        ct[b]+=1
        renorm_freq(ct)
        bq>>=1
    encode_finish(dc)
    return dc.v

def decode_bits(v,sz=64):
    dc=coder_context(v)
    ct=[1,1]
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
    #bi=0b1010101010001000001000000000000010000001111111100000000000000001
    #not adaptive:[252, 154, 25, 112] adaptive [154, 183, 2, 15, 237]
    bi=0b0000001111111111111111111111111111111111111111111111111111111111
    sz=64
    print("inb","{:064b}".format(bi))
    v=encode_bits(bi,sz)
    print("cod",end=' ')
    pall(v)
    b=decode_bits(v,sz)
    print("out","{:064b}".format(b))


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


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
        self.buf=0 # carry for encoder
        self.cnt=0
        self.cnt_rr=0
        self.cnt_rw=0
        
def renorm_and_read(dc):
    dc.cnt_rr+=1
    dc.r*=dc.radix
    dc.l*=dc.radix
    if len(dc.v)>0: dc.l+=dc.v.pop(0)
    dc.l&=MASK

def renorm_and_write(dc):
    dc.cnt_rw+=1
    def put(x):
        dc.v.append(x)
    if dc.l>=dc.max:
        dc.buf+=1
        dc.l&=MASK
        if dc.cnt>0:
            put(dc.buf)
            for _ in range(dc.cnt-1):put(0)
            dc.buf=0
            dc.cnt=0
    while dc.r<dc.radix:
        if dc.l<0xFF<SHIFT:
            put(dc.buf)
            for _ in range(dc.cnt):put(0xff)
            dc.buf=(dc.l&HMSK)>>SHIFT
            dc.cnt=0
        else:
            dc.cnt+=1
        dc.l<<=8
        dc.l&=MASK
        dc.r<<=8

def encode_finish(dc):
    def put(x):
        dc.v.append(x)
    c=0xFF
    if dc.l>=dc.max:
        dc.buf+=1
        c=0x00
    put(dc.buf)
    for _ in range(dc.cnt): put(c)
    q=MASK
    l=dc.l
    while q:
        put((l&HMSK)>>SHIFT)
        l<<=8
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
    print("renorms",dc.cnt_rw)
    return

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
    print("renorms",dc.cnt_rr)
    return bo

def test_enc():
    bi=0b00110000
    sz=8
    v=encode(bi,sz)
    print(v)

def test_dec():
    sz=8
    sq=[128+44,0,1,0,0,0]
    b=decode(sq,sz)
    print("{:08b}".format(b))

if __name__ == "__main__":
    test_enc()
    #test_dec()

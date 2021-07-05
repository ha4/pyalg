#MIN_RANGE=radix
#MAX_RANGE=radix*256
class coder_context:
    def __init__(self,vin,radix=256):
        self.v=vin
        self.radix=radix # also min.range
        self.max=radix*radix
        self.shift=8
        self.r=self.max # code is l/r
        self.l=0
        self.buf=256 # for buffered encoder
        self.cnt=0 # 0xFF carry count
        self.put=lambda y,x: y.append(x)
        self.get=lambda y: y.pop(0)

def renorm_and_read(dc,force=0):
    if dc.r>=dc.radix and not force: return
    #print("r",end='')
    dc.r*=dc.radix
    dc.l*=dc.radix
    if len(dc.v)>0: dc.l+=dc.get(dc.v)
        
def write_and_carry(dc,x,new_buf):
    if dc.buf!=256: dc.put(dc.v,dc.buf&0xFF)
    for _ in range(dc.cnt):dc.put(dc.v,x)
    dc.cnt,dc.buf=0,new_buf

def renorm_and_write(dc):
    if dc.l<dc.max and dc.r>=dc.radix: return
    #print("w",end='')
    msk=dc.max-1
    if dc.l>=dc.max:
        dc.buf,dc.l=dc.buf+1,dc.l&msk
        if dc.cnt>0:
            dc.cnt-=1
            write_and_carry(dc,0x00,0)
    while dc.r<dc.radix:
        x=dc.l>>dc.shift
        if x==0xFF: dc.cnt+=1
        else: write_and_carry(dc,0xFF,x)
        dc.l,dc.r=(dc.l<<8)&msk,dc.r<<8

def encode_finish(dc):
    c=0xFF
    q=msk=dc.max-1
    if dc.l>=dc.max: dc.buf,c,dc.l=dc.buf+1,0x00,dc.l&msk
    write_and_carry(dc,c,256)
    while q and dc.l:
        dc.put(dc.v,dc.l>>dc.shift)
        dc.l,q=(dc.l<<8)&msk,q>>8

def renorm_freq(ct):
    if ct[0]+ct[1]>63-2:
        if ct[0]>1: ct[0]//=2
        if ct[1]>1: ct[1]//=2

# general procedures
def enc_sym(dc,cumf,fs,ftot):
    tmp=dc.r//ftot
    dc.l+=cumf*tmp
    dc.r=fs*tmp
    #dc.l,dc.r=dc.l+dc.r*cumf//ftot,dc.r*fs//ftot
    #renorm_and_write(dc)
def dec_freq(dc,ftot):
    tmp=dc.r//ftot
    return dc.l//tmp
    #return dc.l*ftot//dc.r
def dec_sym(dc,cumf,fs,ftot):
    tmp=dc.r//ftot
    dc.l-=tmp*cumf
    dc.r=tmp*fs
    #dc.l,dc.r=dc.l-dc.r*cumf//ftot,dc.r*fs//ftot
    #renorm_and_read(dc)

#freq procedures
def freq_add(ftbl,sym,f=1):
    fsz=len(ftbl)
    for i in range(sym+1,fsz): ftbl[i]+=f
def freq_renorm(ftbl,limit):
    fsz=len(ftbl)
    while ftbl[-1]>limit:
        for i in range(1,fsz):
            f=ftbl[j]-ftbl[j-1]
            if f==0: continue
            f//=2
            if f==0: f=1
            ftbl[j]=f+ftbl[j-1]
def freq_all(ftbl,lst=[]):
    fsz=len(ftbl)-1
    for j in range(fsz): lst.append(ftbl[j+1]-ftbl[j])
    return lst
def freq_lookup(ftbl,fx):
    a=0
    b=len(ftbl)
    while a<b:
        c=(a+b)//2
        if ftbl[c+1]<=fx: a=c+1
        else: b=c
    return a
def freq_init(symbols,fbase=0):
    fl=[0]*(symbols+1)
    if fbase>0:
        for j in range(symbols): freq_add(fl,fbase)
    return fl

def dec_bit(dc,ct):
    renorm_and_read(dc)
    ft=ct[0]+ct[1]
    spl=dc.r*ct[0]//ft
    b=1 if dc.l>=spl else 0
    if b: dc.l,dc.r=dc.l-spl,dc.r-spl
    else: dc.r=spl
    return b

def enc_bit(dc,ct,b):
    renorm_and_write(dc)
    ft=ct[0]+ct[1]
    spl=dc.r*ct[0]//ft
    if b: dc.l,dc.r=dc.l+spl,dc.r-spl
    else: dc.r=spl

def dec_bitadp(dc,ct):
    b=dec_bit(dc,ct)
    ct[b]+=1
    renorm_freq(ct)
    return b
def enc_bitadp(dc,ct,b):
    enc_bit(dc,ct,b)
    ct[b]+=1
    renorm_freq(ct)

def enc_golomb(dc,ct,num):
    num,ms,lev=num+1,1,0
    while num&((ms<<1)-1)!=num:
        enc_bitadp(dc,ct[1+lev],0)
        ms,lev=ms<<1,lev+1
    enc_bitadp(dc,ct[1+lev],1)
    ms>>=1
    while ms:
        b=1 if num&ms else 0
        enc_bit(dc,ct[0],b)
        ct[0][b]+=1
        renorm_freq(ct[0])
        ms>>=1

def dec_golomb(dc,ct):
    num,b,lev=1,0,0
    while b==0:
        b=dec_bitadp(dc,ct[1+lev])
        lev+=1
    lev-=1
    while lev:
        b=dec_bitadp(dc,ct[0])
        lev,num=lev-1,(num<<1)|b
    return num-1

def encode_bits(bs,sz=64):
    dc=coder_context([])
    ct=[1,1]
    gct=[[1,1] for _ in range(65)]
    enc_golomb(dc,gct,15)
    bq=1<<(sz-1)
    while bq:
        b=1 if bq&bs else 0
        bq>>=1
        enc_bit(dc,ct,b)
        ct[b]+=1
        renorm_freq(ct)
    encode_finish(dc)
    return dc.v

def decode_bits(v,sz=64):
    dc=coder_context(v)
    dc.r=1
    ct=[1,1]
    gct=[[1,1] for _ in range(65)]
    renorm_and_read(dc) # two radix, fill to mask
    renorm_and_read(dc)
    sz2=dec_golomb(dc,gct)
    print(sz2)
    bq,bo=1<<(sz-1),0
    while bq:
        b=dec_bit(dc,ct)
        ct[b]+=1
        renorm_freq(ct)
        if b: bo|=bq
        bq>>=1
    return bo

def lbin(x): return ["{:08b}".format(k) for k in x]

def test_encdec():
    #bi=0b1010101010001000001000000000000010000001111111100000000000000001
    #not adaptive:[252, 154, 25, 112] adaptive [154, 183, 2, 15, 237]
    bi=0b0000001111111111111111111111111111111111111111111111111111111111
    sz=64
    print("inb","{:064b}".format(bi))
    v=encode_bits(bi,sz)
    print("cod",lbin(v))
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

def test_rc_nonadaptive():
    freqs=32
    #insyms=[0,0,5,22,1,5,28,28,5,5,5,0,0]
    insyms=[0,1,2,3,4,5,6,7,8,9,8,7,5,4]
    #insyms=[9,8,7,6,5,4,3,2,1,0]
    lensyms=len(insyms)
    print("ins",insyms,"len",lensyms)
    #coder init
    ec=coder_context([])
    ft=freq_init(freqs)
    for s in insyms: freq_add(ft,s)
    ftot=ft[-1]
    print("tot",ftot)
    print("ftb",freq_all(ft))
    #encode
    for s in insyms:
        print("enc",end=' ')
        ls,fs=ft[s],ft[s+1]-ft[s]
        enc_sym(ec,ls,fs,ftot)
        renorm_and_write(ec)
        print(ls,ec.l,ec.r)
    encode_finish(ec)
    coded=ec.v
    print("cod",coded,"l,r",ec.l,ec.r)
    #decode
    outsyms=[]
    dc=coder_context(coded)
    dc.r=1 # extremly denormalized
    renorm_and_read(dc,1) # two radix, fill to mask
    renorm_and_read(dc,1)
    print("de0",dc.l,dc.r)
    for _ in range(lensyms):
        fx=dec_freq(dc,ftot)
        print("dec",fx,dc.l,dc.r)
        s=freq_lookup(ft,fx)
        dec_sym(dc,ft[s],ft[s+1]-ft[s],ftot)
        renorm_and_read(dc)
        outsyms.append(s)
    print("out",outsyms)


from ac0 import *

if __name__ == "__main__":
    #test_binload()
    #test_diff()
    #test_encdec()
    test_rc_nonadaptive()


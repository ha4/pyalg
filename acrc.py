RC_MAX=0xFFFFFFFF
RC_TOP=0x00FFFFFF
RC_BOT=0x0000FFFF
RC_COD=0x000000FF

# renormalizer & i/o
def rc_input(l,c,v):
    if len(v)<8: v+="0"*(8-len(v))
    rb,v=int(v[:8],2),v[8:]
    c=((c<<8)|rb)&RC_MAX
    return c,v

def rc_output(l,c,v):
    v+="{:08b}".format((l>>24)&RC_COD)
    return c,v

def rc_renorm(l,r,c,v,iof):
    while r<=RC_TOP and ((l^(l+r))<=RC_TOP or r<=RC_BOT and ((r:=(RC_MAX+1-l)&RC_BOT),1)):
        c,v=iof(l,c,v)
        l,r=(l<<8)&RC_MAX,r<<8
    return l,r,c,v

# decoding

def rcd_start(v,iof):
    l,c,r=0,0,RC_MAX
    for _ in range(4):
        c,v=iof(l,c,v)
    return l,r,c,v

def rcd_freq(l,r,c,ft):
    tmp=r//ft
    f=(c-l)//tmp
    return f,tmp

def rcd_dec(l,tmp,ls,rs,ft):
    l+=ls*tmp
    r=tmp*rs
    return l,r

# encoding

def rce_start():
    l,r=0,RC_MAX
    return l,r

def rce_enc(l,r,ls,rs,ft):
    r//=ft
    l+=ls*r
    r*=rs
    return l,r

def rce_fin(l,r,v,iof):
    #print("low","{:032b}".format(l&RC_MAX))
    #print("ran","{:032b}".format(r&RC_MAX))
    while l:
        c,v=iof(l,0,v)
        l=(l<<8)&RC_MAX
    return v

# adaptive bit decoder

def rcd_decode(vo,sz=8):
    bis=0
    l,r,c,v=rcd_start(vo,rc_input)
    ct=[1,1]
    for _ in range(sz):
        ft=ct[0]+ct[1]
        fx,t=rcd_freq(l,r,c,ft)
        b=1 if fx>=ct[0] else 0
        ls,rs=(ct[0],ct[1]) if b else (0,ct[0])
        l,r=rcd_dec(l,t,ls,rs,ft)
        l,r,c,v=rc_renorm(l,r,c,v,rc_input)
        ct[b]+=1
        bis<<=1
        bis|=b
    return bis

# adaptive bit encoder

def rce_encode(bis,sz=8):
    v=""
    l,r=rce_start()
    ct=[1,1]
    bq=1<<(sz-1)
    while bq:
        ft=ct[0]+ct[1]
        b=1 if bis&bq else 0
        ls,rs=(ct[0],ct[1]) if b else (0,ct[0])
        l,r=rce_enc(l,r,ls,rs,ft)
        l,r,c,v=rc_renorm(l,r,0,v,rc_output)
        ct[b]+=1
        bq>>=1
    return rce_fin(l,r,v,rc_output)

# byte frequency table

def freq_add(ftbl,sym):
    fz=len(ftbl)
    for j in range(sym+1,fz):
        ftbl[j]+=1

def freq_lookup(ftbl, f):
    a=0
    b=len(ftbl)
    while a<b:
        c=(a+b)//2
        if ftbl[c+1]<=f: a=c+1
        else: b=c
    return a

def freq_init():
    fx=[0]*257
    for j in range(256): freq_add(fx,j)
    return fx

# file i/o

def get_c(f):
    c = list(f.read(1))
    if len(c)==0: return 0
    return c[0]

def put_c(f, x):
    f.write(bytearray([x & 0xff]))

def rc_finput(l,c,f):
    try:rb=get_c(f)
    except:rb=0
    c=((c<<8)|rb)&RC_MAX
    return c,f

def rc_foutput(l,c,f):
    put_c(f,l>>24)
    return c,f

# adaptive file encoder/decoder

# bit encode

def rce_bit(l,r,ct,b,f,fio):
    ft=ct[0]+ct[1]
    ls,rs=(ct[0],ct[1]) if b else (0,ct[0])
    l,r=rce_enc(l,r,ls,rs,ft)
    l,r,c,f=rc_renorm(l,r,0,f,fio)
    ct[b]+=1
    return l,r,f

def rcd_bit(l,r,c,ct,f,fio):
    ft=ct[0]+ct[1]
    fx,t=rcd_freq(l,r,c,ft)
    b=1 if fx>=ct[0] else 0
    ls,rs=(ct[0],ct[1]) if b else (0,ct[0])
    l,r=rcd_dec(l,t,ls,rs,ft)
    l,r,c,f=rc_renorm(l,r,c,f,fio)
    ct[b]+=1
    return l,r,c,f,b

# golomb number encode/decode

def rce_num(l,r,ct,num,f,fio):
    num=0
    print("enm {:b}".format(num))
    num+=1
    ms=1
    print("glm ",end="")
    while num>ms:
        ms<<=1
        l,r,f=rce_bit(l,r,ct,0,f,fio)
        print("0",end="")
    while ms:
        b=1 if num&ms else 0
        l,r,f=rce_bit(l,r,ct,b,f,fio)
        ms>>=1
        print(b,end='')
    print()
    return l,r,f

def rcd_num(l,r,c,ct,f,fio):
    lev=0
    print("dec ",end='')
    while True:
        l,r,c,f,b=rcd_bit(l,r,c,ct,f,fio)
        print(b,end='')
        if b: break
        lev+=1
    print()
    num=1
    while lev:
        lev-=1
        l,r,c,f,b=rcd_bit(l,r,c,ct,f,fio)
        print(b,end='')
        num=(num<<1)|b
    print()
    print(num)
    return l,r,c,f,num-1

def rce_file(fin,f,sz):
    l,r=rce_start()
    ftab=freq_init()
    btab=[1,1]
    l,r,f=rce_num(l,r,btab,0,f,rc_foutput)
    """
    l,r,f=rce_num(l,r,btab,sz,f,rc_foutput)
    while sz:
        ftot=ftab[-1]
        b=get_c(fin)
        ls=ftab[b]
        rs=ftab[b+1]-ftab[b]
        l,r=rce_enc(l,r,ls,rs,ftot)
        l,r,c,f=rc_renorm(l,r,0,f,rc_foutput)
        freq_add(ftab,b)
        sz-=1
    """
    rce_fin(l,r,f,rc_foutput)

def rcd_file(fin,f):
    l,r,c,fin=rcd_start(fin,rc_finput)
    ftab=freq_init()
    btab=[1,1]
    l,r,c,fin,sz=rcd_num(l,r,c,btab,fin,rc_finput)
    print(sz)
    """
    for _ in range(sz):
        ftot=ftab[-1]
        fx,t=rcd_freq(l,r,c,ftot)
        b=freq_lookup(ftab, fx)
        ls=ftab[b]
        rs=ftab[b+1]-ftab[b]
        l,r=rcd_dec(l,t,ls,rs,ftot)
        l,r,c,fin=rc_renorm(l,r,c,fin,rc_finput)
        freq_add(ftab,b)
        put_c(f,b)
    """

# tests

def test_bits():
    blen=64
    #bii=0b1000000010000000100000001000000010000000111110000000000000000000
    bii=0b1000100011111000101010001000100010001000100010000000000000000000
    #blen=8
    #bii=0b00000000
    #bii=0b11111111
    #bii=0b10000000
    #bii=0b00000001

    print("inp", "{:b}".format(bii))
    co=rce_encode(bii,blen)
    print("got",co,len(co))
    bio=rcd_decode(co,blen)
    print("out","{:b}".format(bio))
    #print("inp","{:b}".format(bii))

import os.path

def test_cfiles(fni,fno):
    size = os.path.getsize(fni)
    inf = open(fni, "rb")
    outf = open(fno, "wb")
    rce_file(inf,outf,size)
    inf.close()
    outf.close()

def test_dfiles(fni,fno):
    size = 768
    inf = open(fni, "rb")
    outf = open(fno, "wb")
    rcd_file(inf,outf)
    inf.close()
    outf.close()


if __name__ == "__main__":
    #test_bits()
    test_cfiles("Cbios_8x8.bin","Cbios_8x8.tmp")
    #test_dfiles("Cbios_8x8.tmp","Cbios_8x8.tm2")

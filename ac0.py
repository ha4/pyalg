from math import *

def readfont(n):
    with open(n,"rb") as f:
        b=list(f.read())
        f.close()
    return b

def chr_i0(a,l=0):
    i0=ord(a)-32
    i0=(i0<0) and 0 or (i0>=95 and 0 or i0)
    return 256*(i0//32)+i0%32+l*32

def chr_data(a,l=None):
    global b
    bs=[]
    if l is None:
        for i in range(8):
            bs.append(b[chr_i0(a,i)])
    else:
        bs.append(b[chr_i0(a,l)])
    return bs

def data2bits(bl,sz=64):
    bb=0
    for bs in bl:
        bc=128
        while bc:
            bb<<=1
            if bs&bc: bb+=1
            bc>>=1
            sz-=1
            if sz==0: return bb
    while sz:
        bb<<=1
        sz-=1
    return bb

def bits2data(bb,sz=64):
    bs=[]
    bg=1<<(sz-1)
    bc=0
    while bg:
        if bc==0:
            bc=128
            bo=0
        if bb&bg:
            bo|=bc
        bg>>=1
        bc>>=1
        if bc==0:
            bs.append(bo)
    if bc:
        bs.append(bo)
    return bs

def freqs_bytes(d,bs):
    tot=0
    for i in bs:
        tot+=1
        try: d[i]+=1
        except: d[i]=1
    return tot

def binstream(bb,sz):
    bq=1<<(sz-1)
    while bq:
        c=(bq&bb) and 1 or 0
        bq>>=1
        yield c

def freqs_bits(d,bb,sz=64):
    tot=0
    for i in binstream(bb,sz):
        tot+=1
        try: d[i]+=1
        except: d[i]=1
    return tot

def freqbin_all(d):
    tt=0
    for i in range(96):
        s=chr(32+i)
        ss=chr_data(s)
        bl=data2bits(ss,64)
        tt+=freqs_bits(d,bl,64)
    return tt

def freqbyte_all(d):
    tt=0
    for i in range(96):
        s=chr(32+i)
        ss=chr_data(s)
        tt+=freqs_bytes(d,ss)
    return tt

def entropy_dict(d,ftot):
    scnt=0
    x=0
    for k,v in d.items():
        scnt+=1
        x+=-v*log(v/ftot,2)
    return scnt,x

def entropy_byte(d,ftot,bb):
    scnt=0
    x=0
    ld={}
    for ss in bb:
        try: ld[ss]+=1
        except: ld[ss]=1
        v=d[ss]
        x+=-log(v/ftot,2)
    return len(ld),x

def entropy_bit(d,ftot,bb,sz=64):
    x=0
    ld={}
    for ss in binstream(bb,sz):
        try: ld[ss]+=1
        except: ld[ss]=1
        v=d[ss]
        x+=-log(v/ftot,2)
    return len(ld),x

b=readfont("Cbios_8x8.bin")

fbin={}
fbin_tot=freqbin_all(fbin)
print("total bits",fbin_tot)

fbins,fbinb=entropy_dict(fbin,fbin_tot)
print("symbols",fbins,"size",fbinb)

fsym={}
fsym_tot=freqbyte_all(fsym)
print("total bytes",fsym_tot)

fsyms,fsymb=entropy_dict(fsym,fsym_tot)
print("symbols",fsyms,"size",fsymb)

sx='%'
cx=chr_data(sx)
xsyms,xsymb=entropy_byte(fsym,fsym_tot,cx)
print("[",sx,"] symbols",xsyms,"size",xsymb)

cbx=data2bits(cx)
xbins,xbinb=entropy_bit(fbin,fbin_tot,cbx,64)
print("[",sx,"] bits",xbins,"size",xbinb)

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

def bits2mat(bb,sz=64):
    bs=[]
    bg=1<<(sz-1)
    while bg:
        bs.append((bb&bg) and 1 or 0)
        bg>>=1
    return bs
    
def mat2bits(bs,sz=64):
    bb=0
    bg=1<<(sz-1)
    while bg:
        if bs.pop(0)>0: bb|=bg
        bg>>=1
    return bb

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

DIRBITS=4
def freqs_chr(d0,d1,bb,sz=64):
    tot0=0
    tot1=0
    bq=1<<(sz-1)
    def get_bit():
        nonlocal bq
        c=(bb&bq) and 1 or 0
        bq>>=1
        return c
    def get_nibl():
        nb=0
        for _ in range(DIRBITS):
            nb=(nb<<1)+get_bit()
        return nb
    while bq:
        b=get_bit()
        #print(b,end=' ')
        tot0+=1
        try: d0[b]+=1
        except: d0[b]=1
        if b:
            nb=get_nibl()
            #print("{:04b}".format(nb),end=' ')
            tot1+=1
            try: d1[nb]+=1
            except: d1[nb]=1
    return tot0,tot1

def freqbyte_all(d):
    tt=0
    for i in range(96):
        s=chr(32+i)
        ss=chr_data(s)
        tt+=freqs_bytes(d,ss)
    return tt

def freqbin_all(d):
    tt=0
    for i in range(96):
        s=chr(32+i)
        ss=chr_data(s)
        bl=data2bits(ss,64)
        tt+=freqs_bits(d,bl,64)
    return tt

def freqchr_all(d0,d1):
    tt0,tt1=0,0
    for i in range(96):
        s=chr(32+i)
        ss=chr_data(s)
        bl=data2bits(ss,64)
        x0,x1=freqs_chr(d0,d1,bl,64)
        tt0+=x0
        tt1+=x1
    return tt0,tt1


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

def entropy_chr(d0,d1,ftot0,ftot1,bb,sz=64):
    x0,x1=0,0
    ld0={}
    ld1={}
    bq=1<<(sz-1)
    def get_bit():
        nonlocal bq
        c=(bb&bq) and 1 or 0
        bq>>=1
        return c
    def get_nibl():
        nb=0
        for _ in range(DIRBITS):
            nb=(nb<<1)+get_bit()
        return nb
    while bq:
        b=get_bit()
        try: ld0[b]+=1
        except: ld0[b]=1
        v=d0[b]
        x0+=-log(v/ftot0,2)
        if b:
            nb=get_nibl()
            try: ld1[nb]+=1
            except: ld1[nb]=1
            v=d1[nb]
            x1+=-log(v/ftot1,2)
    return len(ld0),len(ld1),x0,x1,x0+x1

def fwht(a) -> None:
    """In-place Fast Walsh–Hadamard Transform of array a."""
    h = 1
    while h < len(a):
        for i in range(0, len(a), h * 2):
            for j in range(i, i + h):
                x = a[j]
                y = a[j + h]
                a[j] = x + y
                a[j + h] = x - y
        h *= 2

def fwscl(l,k=4):
    return list(map(lambda x: x/k, l))

# remap list by indices
def imap(f,i):
    bs=[]
    q=len(i)
    for p in range(q):
        yield i[f(p)]

# transpose i,j
def imat_trsp(l,ran=8):
    i,j=l%ran,l//ran
    return j+8*i

# reverse index
def imat_inv(l,ran=8):
    m=ran*ran-1
    return m-l

# offset to i and j
def imat_doffs(l,o=1,ran=8):
    def lim(c): return c%ran
    i,j=l%ran,l//ran
    i=lim(i-o)
    j=lim(j-o)
    return i+8*j

# dublicate or delete column
def imat_vsplit(l,s=1,ran=8):
    dx=(s<0) and -1 or 1
    s=(s<0) and -s or s
    if s==0: dx=0
    s-=1
    def lim(c): return c%ran
    i,j=l%ran,l//ran
    if i-s>=(dx+1)//2: i=lim(i-dx)
    return i+8*j

# diagonal order: 0,0->0,0; 0,1->0,1; 0,2->1,0; 0,3->0,2; 0,4->1,1; 0,5->2,0
def imat_dord(l,ran=8):
    lim=ran*ran-1
    if l*2>lim: return lim-imat_dord(lim-l,ran)
    iv=1
    while l>=iv:
        l-=iv
        iv+=1
    return l*(ran-1)+iv-1

# z-order: 
def imat_zord(l,ran=8):
    lim=ran*ran-1
    if l*2>lim: return lim-imat_zord(lim-l,ran)
    iv=1
    while l>=iv:
        l-=iv
        iv+=1
    if iv&1:
        l=iv-1-l
    return l*(ran-1)+iv-1

# corner snake order: 0,2->1,1; 0,3->1,0; 0,4->2,0; 0,5->2,1; 0,6->2,2; 0,7->1,2
def imat_sord(l,ran=8):
    return l

def prbin(bj): return ("{:08b}".format(bj)).replace("0",".")

def prdata(d):
    for s in d: print(prbin(s))

def prmat(a,ran=8):
    for j in range(0,ran*ran,ran):
        for i in range(ran):
            print("{:3}".format(a[i+j]),end=' ')
        print()

def prpyr(a,ran=8):
    l=len(a)
    j=0
    iv=0
    while j<l:
        iv+=(j<32) and 1 or -1
        for i in range(iv):
            print("{:3}".format(a[i+j]),end=' ')
        print()
        j+=iv

def diff_v(bs,revers=0):
    bu=[]
    pd=0xff if revers else 0
    p=0
    for sl in bs:
        bu.append(p^sl)
        p=(pd&p)^sl
    return bu

def diff_h(bs,revers=0):
    bu=[]
    pd=0xff if revers else 0
    for sl in bs:
        bp,bo,bq=0,0,128
        while bq:
            bo|=((bp>>1)^sl)&bq
            bp,bq=(((bp>>1)&pd)^sl)&bq,bq>>1
        bu.append(bo)
    return bu

from fontcomp import patchfnt

def test_binload(patch=True):
    global b
    global cx
    global cbx
    b=readfont("Cbios_8x8.bin")
    if patch: patchfnt(b)
    cx=chr_data(sx)
    cbx=data2bits(cx)
    
def test_dict():

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

    xsyms,xsymb=entropy_byte(fsym,fsym_tot,cx)
    print("[",sx,"] symbols",xsyms,"size",xsymb)

    xbins,xbinb=entropy_bit(fbin,fbin_tot,cbx,64)
    print("[",sx,"] bits",xbins,"size",xbinb)

    d0={}
    d1={}
    #f0_tot,f1_tot=freqs_chr(d0,d1,cbx)
    f0_tot,f1_tot=freqchr_all(d0,d1)
    print("total bits",f0_tot,"total nibs",f1_tot)

    f0s,f0b=entropy_dict(d0,f0_tot)
    f1s,f1b=entropy_dict(d1,f1_tot)
    print("singlebit",f0s,"size",f0b,"nibbles",f1s,"size",f1b,"sumsize",f0b+f1b)

    xbits,xnibs,xbitb,xnibb,xsumb=entropy_chr(d0,d1,f0_tot,f1_tot,cbx,64)
    print("[",sx,"] bits",xbits,"size",xbitb, "nibls",xnibs, "size",xnibb,"total",xsumb)

def test_transform():
    cmx=bits2mat(cbx)
    cwx=cmx.copy()
    cwx=list(imap(lambda x: imat_doffs(x,1), cwx))
    cwx=list(imap(lambda x: imat_vsplit(x,4), cwx))
    fwht(cwx)
    cwx[6]=-6
    #cwx[63]=0
    #cwy=fwscl(cwx)
    #cwy=cwx.copy()
    cwx=list(map(lambda x: x//4, cwx))
#    cwx=list(map(lambda x: -x, cwx))
    cwx[0]=-1
    #cwx=list(map(lambda x: 0, cwx))
    #cwx[0]=-1
    #cwx=list(imap(imat_trsp, cwx))
    #cwx=list(imap(imat_inv, cwx))
    cwz=list(imap(imat_zord, cwx))
    prmat(cwx)
    print(cwz)
#    cwx=cwz

    dwt={}
    dwt_tot=freqs_bytes(dwt,cwx)
    print("total functs",dwt_tot)
    fws,fwb=entropy_dict(dwt,dwt_tot)
    print("symbols",fws,"size",fwb)

    fwht(cwx)
    cwx=list(imap(lambda x: imat_vsplit(x,-4), cwx))
    cwx=list(imap(lambda x: imat_doffs(x,-1), cwx))

    ccy=mat2bits(cwx)
    cy=bits2data(ccy)
    prdata(cy)

def test_walsh():
    m1=[0]*64
    m1[0*8+7]=1
    m1[2*8+7]=1
    m1[4*8+7]=1
    m1[6*8+7]=1
    prmat(m1)
    fwht(m1)
    prmat(m1)
    prdata(bits2data(mat2bits(m1)))

def test_forwrev():
    m0=[x for x in range(64)]
    fwht(m0)
    m0=list(map(lambda x: x//8, m0))
    fwht(m0)
    m0=list(map(lambda x: x//8, m0))
    prmat(m0)

def test_idx():
    m0=[0]*64
    m1=list(range(64))
    # fill diagonal
    for i in range(64):
        p,r=i,1 # repeated transform
        while r: p,r=imat_zord(p),r-1
        m0[p]=i
    # doiagonal traversal
    m0=list(imap(imat_zord,m0))
    prmat(m0)
    #prpyr(m0)

def test_diff():
    e1=cx
    e1=diff_v(e1)
    e1=diff_h(e1)
    prdata(e1)
    
    cmx=bits2mat(data2bits(e1))
    cmx=list(imap(lambda x: imat_doffs(x,1), cmx))
    cmx=list(imap(lambda x: imat_vsplit(x,4), cmx))
    fwht(cmx)
    cmx=list(map(lambda x: int(x//4), cmx))
    cmx[0]=0
    prmat(cmx)
    #print(list(imap(imat_zord, cmx)))
    
    wt={}
    wt_tot=freqs_bytes(wt,cmx)
    print("total functs",wt_tot)
    fws,fwb=entropy_dict(wt,wt_tot)
    print("symbols",fws,"size",fwb)

    #zz=[0, 0, 0, 0, 0, -1, 0, 0, -1, -1, 0, 0, 0, 0, 0, -1, 0, -1, -1, 0, -1, -1, 0, 0, 0, 0, 0, -1, -1, 0, 0, 0, 0, -1, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, -1, 0, 0]
    #cmt=[0]*len(zz)
    #for i in range(len(zz)): cmt[imat_zord(i)]=zz[i]
    cmt=cmx
    fwht(cmt)
    cmt=list(imap(lambda x: imat_vsplit(x,-4), cmt))
    cmt=list(imap(lambda x: imat_doffs(x,-1), cmt))
    e2=bits2data(mat2bits(cmt))
    e2=diff_h(e2,1)
    e2=diff_v(e2,1)
    prdata(e2)
    

sx='M'

if __name__ == "__main__":
    test_binload()
    #test_dict()
    #test_transform()
    #test_walsh()
    #test_forwrev()
    #test_idx()
    test_diff()


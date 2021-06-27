import os
import math

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


def prbin(bj): return ("{:08b}".format(bj)).replace("0",".")

def prindata(bs):
    for e in bs: print(prbin(e))

def prinstr(a):
    for l in range(8):
        for s in a:
            print(prbin(chr_data(s,l)[0]),end=' ')
        print()

def binstream(bt):
    for s in bt:
        bc=128
        while bc:
            sb = (bc&s) and 1 or 0
            bc>>=1
            yield sb

def prstream(cd):
    for bx in binstream(cd):
        print(bx,end='')
    print()

RADIX=256
def rcomp(cd):
    ct=[0,0]
    l=0
    r=RADIX
    ob=""
    def renorm(l,r,v):
        print("[renormE ",end='')
        vx=""
        while r<RADIX:
            if l>=RADIX:
                if l>=2*RADIX:
                    vx+="1"
                    l-=RADIX
                l-=RADIX
            else:
                vx+="0"
            l*=2
            r*=2
            print(end=',')
        print(l,r,vx,end=']')
        return l,r,v+vx
    for bx in binstream(cd):
        ft=ct[0]+ct[1]+2
        print(l,r,"- ",end='')
        if bx:
            l+=(ct[0]+1)*r//ft
            r=(ct[1]+1)*r//ft
        else:
            l+=0*r//ft
            r=(ct[0]+1)*r//ft
        ct[bx]+=1
        print(bx,"->",l,r,ct,end='')
        if r<RADIX:
            l,r,ob=renorm(l,r,ob)
        print()
    print(l,r,end=' ')
    l,r,ob=renorm(l,1,ob)
    print()
    return ob

def rdeco(v):
    cd=[]
    ct=[1,1,0]
    l=0
    r=1
    def renorm(l,r,v):
        print("[renormD ",end='')
        vx=""
        while r<RADIX:
            r*=2
            l*=2
            l+=int(v[0],2)
            vx+=v[0]
            v=v[1:]
            print(end="'")
        print(l,r,vx,end=']')
        return l,r,v
    for _ in range(64):
        print(l,r,end='')
        if r<RADIX:
            l,r,v=renorm(l,r,v)
        ft=ct[0]+ct[1]+2
        spl=r*(ct[0]+1)//ft
        r//=ft        
        bx=l>=spl and 1 or 0
        print("",spl,bx)
        if bx:
            l+=(ct[0]+1)*r
            r*=ct[1]+1
        else:
            r*=ct[0]+1
        print()
        ct[bx]+=1
        cd.append(bx)
    return cd

#
#unnormalized range arithmetic adaptive coding
#

def prinlong(f): print("{:.20f} {:055b}".format(f,int(f*(1<<55))))

def enc_bit(l,r,b,ct):
    ft=ct[0]+ct[1]
    spl=(ct[0])/ft
    ls,rs=(b and spl or 0),(ct[b])/ft
    l,r=l+ls*r, rs*r
    #print("{:11.9} {:11.9} {}".format(l,r,b))
    return l,r

def dec_bit0(code,ct):
    ft=ct[0]+ct[1]
    spl=(ct[0])/ft
    dc=code-spl
    b=dc>=0 and 1 or 0
    #print("{:11.9} {:11.9} {} {:11.9} {}".format(code,spl,ct,dc,b))
    ls,rs=(b and spl or 0),(ct[b])/ft
    return b,(code-ls)/rs

def dec_bit(code,l,r,ct):
    ft=ct[0]+ct[1]
    spl=(ct[0])/ft
    c1=(code-l)/r
    dc=c1-spl
    b=(dc>=-1e-15) and 1 or 0
    #print("{:11.9} {:11.9} {} {:11.9} {}".format(c1,spl,ct,dc,b))
    ls,rs=(b and spl or 0),(ct[b])/ft
    return b,l+ls*r, rs*r

def enc_bits(bb):
    ct=[1,1]
    l,r=0.0,1.0
    bc=128
    while bc:
        sb = (bc&bb) and 1 or 0
        bc>>=1
        l,r=enc_bit(l,r,sb,ct)
        ct[sb]+=1
        #print(sb,l,r,ct)
    return l

def dec_bits(code):
    ct=[1,1]
    l,r=0.0,1.0
    bb=0
    bc=128
    while bc:
        #sb,code = dec_bit0(code,ct)
        sb,l,r = dec_bit(code,l,r,ct)
        ct[sb]+=1
        if sb: bb|=bc
        bc>>=1
        #print(sb,code,l,r,ct)
    return bb

def dec_bits0(code):
    ct=[1,1]
    l,r=0.0,1.0
    bb=0
    bc=128
    while bc:
        sb,code = dec_bit0(code,ct)
        ct[sb]+=1
        if sb: bb|=bc
        bc>>=1
        #print(sb,code,l,r,ct)
    return bb

def enc_bytes(bs):
    ct=[1,1]
    l,r=0.0,1.0
    for bb in bs:
        bc=128
        while bc:
            sb = (bc&bb) and 1 or 0
            bc>>=1
            l,r=enc_bit(l,r,sb,ct)
            ct[sb]+=1
            #print(sb,l,r,ct)
    #print(ct)
    #prinlong(r)
    return l

def dec_bytes(code):
    ct=[1,1]
    bo=[]
    l,r=0.0,1.0
    for _ in range(8):
        bc=128
        bb=0
        while bc:
            #sb,code = dec_bit0(code,ct)
            sb,l,r = dec_bit(code,l,r,ct)
            ct[sb]+=1
            if sb: bb|=bc
            bc>>=1
            #print(sb,code,ct)
        bo.append(bb)
    #print(ct)
    return bo

CTXSW=5
def enc_chr(bs):
    ct0=[1,1]
    ct1=[1,1]
    l,r=0.0,1.0
    cnt=0
    for bb in bs:
        bc=128
        while bc:
            sb = (bc&bb) and 1 or 0
            bc>>=1
            if cnt==0:
                l,r=enc_bit(l,r,sb,ct0)
                ct0[sb]+=1
            else:
                l,r=enc_bit(l,r,sb,ct1)
                ct1[sb]+=1
                cnt-=1
            if sb: cnt=CTXSW
            #print(sb,l,r,ct)
    #print(ct0,ct1)
    #prinlong(r)
    return l

def dec_chr(code):
    ct0=[1,1]
    ct1=[1,1]
    bo=[]
    l,r=0.0,1.0
    cnt=0
    for _ in range(8):
        bc=128
        bb=0
        while bc:
            if cnt==0:
                sb,code = dec_bit0(code,ct0)
                #sb,l,r = dec_bit(code,l,r,ct0)
                ct0[sb]+=1
            else:
                sb,code = dec_bit0(code,ct1)
                #sb,l,r = dec_bit(code,l,r,ct1)
                ct1[sb]+=1
                cnt-=1
            if sb: cnt=CTXSW
            if sb: bb|=bc
            bc>>=1
            #print(sb,code,ct)
        bo.append(bb)
    #print(ct0,ct1)
    return bo
    
print(os.getcwd())
b=readfont("Cbios_8x8.bin")
#prinstr("Imprintabl")
#cd=chr_data('a',4)
#print(prbin(cd[0]))
#o=rcomp(cd)
#print(len(o),o)
#r=rdeco(o)
#print(r)


#bii=0b11110100
#bii=248
#print("{:b}".format(bii))
#cw=enc_bits(bii)
#prinlong(cw)
#bio=dec_bits(cw)
#print("{:b}".format(bio))
#bi0=dec_bits0(cw)
#print("{:b}".format(bi0))

bi=chr_data('=')
#print(bi)
#cw=enc_bytes(bi)
#cw=enc_chr(bi)
#prinlong(cw)
#bo=dec_bytes(cw)
#bo=dec_chr(cw)
#print(bo)

fq={}

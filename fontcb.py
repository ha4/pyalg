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

def chr_data(a):
    global b
    bs=[]
    for i in range(8):
        bs.append(b[chr_i0(a,i)])
    return bs

def prbin(bj): return ("{:08b}".format(bj)).replace("0",".")

def prindata(bs):
    for e in bs: print(prbin(e))

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

RADIX=1968
def rcomp(a):
    cd=chr_data(a)
    ct=[1,1,0]
    l=0
    r=RADIX
    ob=[]
    def renorm(l,r):
        ob.append(l%RADIX)
        r*=RADIX
        l%=RADIX
        return l,r
    for bx in binstream(cd):
        ft=ct[0]+ct[1]
        spl=r*ct[0]//ft
        if bx:
            l+=spl
            r+=spl
        else:
            r=spl
        if r<RADIX:
            l,r=renorm(l,r)
        ct[bx]+=1
        print(l,r,ct[0],ct[1])
    ob.append(l%RADIX)
    l//=RADIX
    ob.append(l)
    ob.append(0)
    return ob
def rdeco(v):
    cd=[]
    ct=[0,0,0]
    l=0
    r=1
    def renorm(l,r,v):
        print("renorm")
        r*=RADIX
        l*=RADIX
        l+=v[0]
        print(l,r)
        return l,r,v[1:]
    for _ in range(64):
        if r < RADIX:
            l,r,v=renorm(l,r,v)
        ft=ct[0]+ct[1]+2
        spl=r*(ct[0]+1)//ft
        bx=l>=spl and 1 or 0
        if bx:
            l-=spl
            r-=spl
        else:
            r=spl
        cd.append(bx)
        print(len(cd),cd)
    return cd

print(os.getcwd())
b=readfont("Cbios_8x8.bin")

o=rcomp('k')
print(len(o),o)
#r=rdeco(o)
#print(r)

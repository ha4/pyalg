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

RADIX=256
def rcomp(a):
    cd=chr_data(a)
    ct=[0,0]
    l=0
    r=RADIX-1
    ob=""
    def renorm(l,r,v):
        #print("renormE")
        while r<RADIX:
            if l>RADIX:
                if l>=2*RADIX:
                    v+="1"
                    l-=2*RADIX
                else:
                    l-=RADIX
            else:
                v+="0"
            l*=2
            r*=2
        return l,r,v
    for bx in binstream(cd):
        ft=ct[0]+ct[1]+2
        #spl=r*ct[0]//ft
        r//=ft
        if bx:
            l+=(ct[0]+1)*r
            r*=ct[1]+1
        else:
            l+=0*r
            r*=ct[0]+1
        l,r,ob=renorm(l,r,ob)
        ct[bx]+=1
        print(bx,l,r,ct[0],ct[1])
    return ob
def rdeco(v):
    cd=[]
    ct=[1,1,0]
    l=0
    r=RADIX-1
    def renorm(l,r,v):
        #print("renormD")
        while r<RADIX:
            r*=2
            l*=2
            l+=int(v[0],2)
            v=v[1:]
            print("renormD l,r",l,r,v)
        return l,r,v
    for _ in range(64):
        l,r,v=renorm(l,r,v)
        ft=ct[0]+ct[1]+2
        spl=r*(ct[0]+1)//ft
        print("l,r,spl",l,r,spl)
        r//=ft        
        bx=l>=spl and 1 or 0
        if bx:
            l+=(ct[0]+1)*r
            r*=ct[1]+1
        else:
            r*=ct[0]+1
        ct[bx]+=1
        cd.append(bx)
        print(bx)
    return cd

print(os.getcwd())
b=readfont("Cbios_8x8.bin")

o=rcomp('k')
print(len(o),o)
r=rdeco(o)
print(r)

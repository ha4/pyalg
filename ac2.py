#
# range arithmetic adaptive coding with renormalization
#

def PL(f): return "{:<.20f} {:056b}".format(f,int(f*(1<<55)))
def PF(f): return "{:056b}".format(int(f*(1<<55)))
def PX(f): return "{:<10.6}".format(f)
from math import log
def EB2(n,m): return -n*log(n/m,2)-(m-n)*log((m-n)/m,2)
def EB(*freqs): return sum(map(lambda n:-n*log(n/sum(freqs),2),freqs))

def enc_renorm(l,r,v):
    while r<.5:
        l*=2
        r*=2
        #print("r9e LLL{:-10.6}".format(l),end=' ')
        oc=int(l)
        l-=oc
        v.append(oc)
    #if len(v):  print("r9e L{:<10.6} H{:<10.6} r{:<10.6} {}".format(l,l+r,r,v))
    return l,r,v

def dec_renorm(code,l,r,v):
    while r<.5:
        l*=2
        l-=int(l)
        r*=2
        code*=2
        code-=int(code)
        ic=int(v.pop(0))
        code+=ic/2
    return code,l,r,v

def enc_bit(l,r,b,ct):
    ft=ct[0]+ct[1]
    spl=(ct[0])/ft
    ls,rs=(spl if b else 0.0),(ct[b])/ft
    l,r=l+ls*r, rs*r
    #print("bit",b,"ls",PX(ls),"rs",PX(rs))
    #print("low",PF(l))
    #print("ran",PF(r))
    #print(" hi",PF(l+r))
    return l,r

def dec_bit(code,l,r,ct):
    ft=ct[0]+ct[1]
    spl=(ct[0])/ft
    dc=(code-l)-spl
    return 1 if dc>=0 else 0

def enc_bits(bb,sz=8):
    bc=1<<(sz-1)
    do=[]
    ct=[1,1]
    l,r=0.0,1.0
    while bc:
        sb = 1 if (bc&bb) else 0
        bc>>=1
        l,r=enc_bit(l,r,sb,ct)
        ct[sb]+=1
        if r<0.1: l,r,do=enc_renorm(l,r,do)
        #print(sb,l,r,ct)
    l,r,do=enc_renorm(l,r,do)
    return do

def dec_bits(di,sz=8):
    bc=1<<(sz-1)
    bb=0
    ct=[1,1]
    l,r=0.0,1.0
    code=0
    code,l,r,di=dec_renorm(code,l,r,di)
    print(PL(code))
    while bc:
        sb=dec_bit(code,l,r,ct)
        l,r=enc_bit(l,r,sb,ct)
        ct[sb]+=1
        if r<0.1: code,l,r,di=dec_renorm(code,l,r,di)
        if sb: bb|=bc
        bc>>=1
    return bb

#from acrc import *

if __name__ == "__main__":
    #bii=0b1000000010000000100000001000000010000000111110000000000000000000
    # out 1000001011110100000110000010111101100000110(43)
    #bii=0b1000100011111000101010001000100010001000100010000000000000000000
    #bii=0b00000000  #outbits:000      0(non-adaptive)
    #bii=0b11111111  #outbits:111      0(non-adaptive)
    #bii=0b11110100  #outbits:11001111 110111(non-adaptive)
    #bii=0b10000000  #outbits:100000   1110(non-adaptive)
    #bii=0b01000000  #outbits:010101
    #bii=0b00100000  #outbits:010000
    bii=0b00010000  #outbits:001100
    #bii=0b00001000  #outbits:001010
    #bii=0b00000100  #outbits:001001
    #bii=0b00000010  #outbits:001000
    #bii=0b00000001  #outbits:000111   01(non adaptive)
    #bii=0b10000100  #outbits:1000011  101111(non adaptive)
    #bii=0b10001000  #outbits:1000100
    #bii=248
    sz=8
    
    print("inp", "{:b}".format(bii))
    co=enc_bits(bii,sz)
    print("got",co,len(co))
    bio=dec_bits(co,sz)
    print("out","{:b}".format(bio))

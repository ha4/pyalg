#
# range arithmetic adaptive coding with renormalizatiob
#

def PL(f): return "{:<.20f} {:056b}".format(f,int(f*(1<<55)))
def PF(f): return "{:056b}".format(int(f*(1<<55)))
def PX(f): return "{:<10.6}".format(f)
from math import log
def EB2(n,m): return -n*log(n/m,2)-(m-n)*log((m-n)/m,2)
def EB(*freqs): return sum(map(lambda n:-n*log(n/sum(freqs),2),freqs))

def enc_renorm(l,r):
    v=""
    while r<.5:
        l*=2
        r*=2
        #print("r9e LLL{:-10.6}".format(l),end=' ')
        oc=int(l)
        l-=oc
        v=str(oc)
    #if len(v):  print("r9e L{:<10.6} H{:<10.6} r{:<10.6} {}".format(l,l+r,r,v))
    return l,r,v

def enc_bit(l,r,b,ct):
    v=""
    ft=ct[0]+ct[1]
    spl=(ct[0])/ft
    ls,rs=(spl if b else 0.0),(ct[b])/ft
    l,r=l+ls*r, rs*r
    """
    print("bit",b,"ls",PX(ls),"rs",PX(rs))
    print("low",PF(l))
    print("ran",PF(r))
    print(" hi",PF(l+r))
    """
    #l,r,v=enc_renorm(l,r)
    return l,r,v

def dec_bit(code,ct):
    ft=ct[0]+ct[1]
    spl=(ct[0])/ft
    dc=code-spl
    b=1 if dc>=0 else 0
    #print("{:11.9} {:11.9} {} {:11.9} {}".format(code,spl,ct,dc,b))
    ls,rs=(spl if b else 0),(ct[b])/ft
    return b,(code-ls)/rs

def enc_bits(bb,sz=8):
    lo=""
    ct=[1,1]
    l,r=0.0,1.0
    bc=1<<(sz-1)
    while bc:
        sb = 1 if (bc&bb) else 0
        bc>>=1
        l,r,v=enc_bit(l,r,sb,ct)
        lo+=v
        ct[sb]+=1
        #print(sb,l,r,ct)
    return l,lo

def dec_bits(code,sz=8):
    ct=[1,1]
    l,r=0.0,1.0
    bb=0
    bc=1<<(sz-1)
    while bc:
        sb,code = dec_bit(code,ct)
        ct[sb]+=1
        if sb: bb|=bc
        bc>>=1
        #print(sb,code,l,r,ct)
    return bb

from acrc import *

if __name__ == "__main__":
    #bii=0b1000000010000000100000001000000010000000111110000000000000000000
    # out 1000001011110100000110000010111101100000110(43)
    bii=0b1000100011111000101010001000100010001000100010000000000000000000
    #bii=0b00000000  #outbits:000 0(non-adaptive)
    #bii=0b11111111  #outbits:111 0(non-adaptive)
    #bii=0b11110100  #outbits:11001111 110111(non-adaptive)
    #bii=0b10000000  #outbits:100000   1110(non-adaptive)
    #bii=0b00000001  #outbits:000111   01(non adaptive)
    #bii=0b10000100  #outbits:1000011  101111(non adaptive)
    
    #bii=248
    #print("inp", "{:b}".format(bii))
    #cw,co=enc_bits(bii)
    #cw,co=enc_bits(bii,64)
    co=rce_encode(bii,64)
    #co=rce_encode(bii)
    print("got",co,len(co))
    #cw=int(co,2)/(1<<len(co))
    #print("cod",PL(cw))
    #bio=dec_bits(cw)
    #bio=dec_bits(cw,64)
    bio=rcd_decode(co,64)
    #bio=rcd_decode(co,8)
    print("out","{:b}".format(bio))
    print("inp","{:b}".format(bii))

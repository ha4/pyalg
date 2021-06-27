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

def dec_bit(code,ct):
    ft=ct[0]+ct[1]
    spl=(ct[0])/ft
    dc=code-spl
    b=dc>=0 and 1 or 0
    #print("{:11.9} {:11.9} {} {:11.9} {}".format(code,spl,ct,dc,b))
    ls,rs=(b and spl or 0),(ct[b])/ft
    return b,(code-ls)/rs

def enc_bits(bb,sz=8):
    ct=[1,1]
    l,r=0.0,1.0
    bc=1<<(sz-1)
    while bc:
        sb = (bc&bb) and 1 or 0
        bc>>=1
        l,r=enc_bit(l,r,sb,ct)
        ct[sb]+=1
        #print(sb,l,r,ct)
    return l

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


bii=0b11110100
#bii=248
print("{:b}".format(bii))
cw=enc_bits(bii)
prinlong(cw)
bio=dec_bits(cw)
print("{:b}".format(bio))

import os
import math

def readfont(n):
    with open(n,"rb") as f:
        b=list(f.read())
        f.close()
    return b

def chr_i0(a):
    i0=ord(a)-32
    i0=(i0<0) and 0 or (i0>=95 and 0 or i0)
    return 256*(i0//32)+i0%32

def i_chr(i): return chr(32+i%32+32*(i//256))

def i_i0(i): return i%32+256*(i//256),(i//32)%8

def chr_data(a):
    global b
    bs=[]
    i0=chr_i0(a)
    for i in range(8):
        bs.append(b[i*32+i0])
    return bs

def chr_nibs(a):
    global b
    bs=[]
    i0=chr_i0(a)
    for i in range(8):
        j=b[i*32+i0]
        bs.append(j>>4)
        bs.append(j&15)
    return bs

def chr_bits(a):
    global b
    bs=""
    i0=chr_i0(a)
    for i in range(8):
        bs+="{:08b}".format(b[i*32+i0])
    return bs

def freqs(lst):
    f={}
    for i in lst:
        try: f[i]+=1
        except: f[i]=1
    return f

def freqnib(lst):
    f={}
    for i in lst:
        n=i>>4;
        try: f[n]+=1
        except: f[n]=1
        n=i&15;
        try: f[n]+=1
        except: f[n]=1
    return f

def freqsb(lst):
    f={}
    f['0']=0
    f['1']=0
    for i in lst:
        for b in "{:08b}".format(i):
            f[b]+=1
    return f

def symap(f): return sorted(f, key=f.get, reverse=True)
def symap2(f): return sorted(f, key=f.get)

def rangs(mp,fq):
    rs=[]
    r=0
    for s in mp:
       rs.append(r)
       r+=fq[s]
    rs.append(r)
    return rs,r

def prindict(m,f,full=False):
    ft=0
    for e in m:
        ft+=f[e]
        if full: print("{:3} {:08b} {}".format(e, e, f[e]))
    if full: print("map:",m)
    print('dict sz:',len(m),'freqsum',ft)

def prbin(bj): return ("{:08b}".format(bj)).replace("0",".")

def prindata(bs):
    for e in bs:
        print(prbin(e))

def princhr(a):
    global c
    global b
    i0=chr_i0(a)
    for i in range(8):
        j=i*32+i0
        print("{} {:03} {} {:8} {:3} {}".format(a,j,i,prbin(b[j]),b[j],c[b[j]]))

def prinstr(s):
    global b
    for c in s:
        print("{:8} ".format(c),end='')
    print()
    for i in range(8):
        for c in s:
            i0=chr_i0(c)+i*32
            print("{} ".format(prbin(b[i0])),end='')
        print()

# 24 values
def huff45(i):
    if i<8: return "{:04b}".format(i+8)
    else:   return "{:05b}".format(i-8)
def dehff45(s):
    if s[0]=='1':return int(s[0:4],2)-8,s[4:]
    else:        return int(s[0:5],2)+8,s[5:]

# 36 values
def huff36(i):
    if i<4:      return "{:03b}".format(i+4)
    else:        return "{:06b}".format(i)
def dehff36(s):
    if s[0]=='1':return int(s[0:3],2)-4,s[3:]
    else:        return int(s[0:6],2),s[6:]

# 20 values
def huff35(i):
    if i<4:      return "{:03b}".format(i+4)
    else:        return "{:05b}".format(i-4)
def dehff35(s):
    if s[0]=='1':return int(s[0:3],2)-4,s[3:]
    else:        return int(s[0:5],2)+4,s[5:]

# 24 values
def huff346(i):
    if i<4:      return "{:03b}".format(i+4)
    elif i<8:    return "{:04b}".format(i)
    else:        return "{:06b}".format(i-8)
def dehff346(s):
    if s[0]=='1':return int(s[0:3],2)-4,s[3:]
    elif s[1]=='1':return int(s[0:4],2),s[4:]
    else:        return int(s[0:6],2)+8,s[6:]

# 22 values
def huff246(i):
    if i<2:    return "{:02b}".format(i+2)
    elif i<6:  return "{:04b}".format(i+2)
    else:      return "{:06b}".format(i-6)
def dehff246(s):
    if s[0]=='1':return int(s[0:2],2)-2,s[2:]
    elif s[1]=='1': return int(s[0:4],2)-2,s[4:]
    else:        return int(s[0:6],2)+6,s[6:]

# 28 values
def huff3457(i):
    if i<4:     return "{:03b}".format(i+4)
    elif i<8:   return "{:04b}".format(i)
    elif i<12:  return "{:05b}".format(i-4)
    else:       return "{:07b}".format(i-12)
def dehff3457(s):
    if s[0]=='1':  return int(s[0:3],2)-4,s[3:]
    elif s[1]=='1':return int(s[0:4],2),s[4:]
    elif s[2]=='1':return int(s[0:5],2)+4,s[5:]
    else:          return int(s[0:7],2)+12,s[7:]

# 20 values
def huff3456(i):
    if i<4:     return "{:03b}".format(i+4)
    elif i<8:   return "{:04b}".format(i)
    elif i<12:  return "{:05b}".format(i-4)
    else:       return "{:06b}".format(i-12)
def dehff3456(s):
    if s[0]=='1':  return int(s[0:3],2)-4,s[3:]
    elif s[1]=='1':return int(s[0:4],2),s[4:]
    elif s[2]=='1':return int(s[0:5],2)+4,s[5:]
    else:          return int(s[0:6],2)+12,s[6:]

# 29 values
def huff1467(i):
    if i==0:  return "1"
    elif i<5: return "{:04b}".format(i+3)
    elif i<13:return "{:06b}".format(i+3)
    else:     return "{:07b}".format(i-13)
def dehff1467(s):
    if s[0]=='1':  return 0,s[1:]
    elif s[1]=='1':return int(s[0:4],2)-3,s[4:]
    elif s[2]=='1':return int(s[0:6],2)-3,s[6:]
    else:          return int(s[0:7],2)+13,s[7:]

# 23 values
def huff1357(i):
    if i==0:  return "1"
    elif i<3: return "{:03b}".format(i+1)
    elif i<7: return "{:05b}".format(i+1)
    else:     return "{:07b}".format(i-7)
def dehff1357(s):
    if s[0]=='1':  return 0,s[1:]
    elif s[1]=='1':return int(s[0:3],2)-1,s[3:]
    elif s[2]=='1':return int(s[0:5],2)-1,s[5:]
    else:          return int(s[0:7],2)+7,s[7:]

def pakdata(m,bs):
    p=''
    for e in bs:
        n=m.index(e)
        p+=huff(n) #+' '
    return p

def unpdata(m,p):
    bs=[]
    for e in range(8):
        v,p=dehff(p)
        bs.append(m[v])
    return bs

def prinbytein(x):
    global b
    try:
        j=b.index(x)
        print('byte:',x,'@',j,i_chr(j),'offset:',i_i0(j))
    except:
        print("not-found")

def patchfnt():
    global b

    # < 24
    b[60]=16
    b[188]=16
    # > 192
    b[62]=64
    b[190]=64
    # % 208,88
    b[37]-=64
    b[69]-=128+64
    b[133]-=16+8
    b[165]-=16
    # J 56
    b[266]=120
    # l 192
    b[524]+=32
    b[556]=32
    b[588]=32
    b[620]=32
    b[652]=32
    b[684]=32
    # r 192
    b[626]+=8-64
    b[594]-=8-64
    # $ 40
    b[132]=8
    # $ 160
    b[68]=128
    # &
    b[6]-=32
    b[38]+=16
    b[70]-=32
    b[134]-=8
    b[166]+=8
    # D
    b[292]+=64
    b[324]+=64
    b[356]+=64
    b[388]+=64
    # G
    b[359]-=32
    # M
    b[269]-=64+16
    b[301]+=64+16
    #W
    b[439]-=64+16
    b[407]+=64+16
    #w
    b[695]-=64+16
    b[663]+=64+16
    #j
    b[522]<<=1
    b[586]<<=1
    b[618]<<=1
    b[650]<<=1
    b[682]<<=1
    b[714]<<=1
    b[746]=(b[746]-64)<<1
    #N
    b[270]-=64
    #b[302]+=64
    #x
    b[600]-=64
    b[632]+=64
    b[664]=136 #96
    b[696]-=16
    #a
    b[577]-=16
    b[609]+=16
    #f
    b[518]=b[518]-16 >> 1
    b[550]=b[550]-8 >> 1
    b[582]>>=1
    b[614]>>=1
    b[646]>>=1
    b[678]>>=1
    b[710]>>=1
    b[742]-=64
    #t
    b[660]-=8
    #4
    b[20]+=16
    b[52]+=32+16
    b[84]+=64+16
    b[148]+=16
    b[180]+=16

    #test
    #b[166]=0
    #b[433]=0

def testhuff(f,g):
    tl=0
    for i in range(24):
        sq=f(i)
        n2,s=g(sq)
        tl+=len(sq)
        print("{:2}".format(i),"{:2}".format(n2),sq)
    print("totallen:",tl)

def testall():
    global m
    tl=0
    tll=0
    ml=0
    nl=100
    for i in range(96):
        s=chr(32+i)
        ss=chr_data(s)
        ps=pakdata(m,ss)
        ls=len(ps)
        ml=max(ml,ls)
        nl=min(nl,ls)
        tl+=ls
        tll+=ls*ls
        print(s,ls,ps)
    al=tl/96
    print(tl, al, math.sqrt(tll/96-al*al), nl, ml)


def ransenc_ss(code,cum_freq,symb_fq,fq_total): # 
    p=""
    #xmax=32
    #renormalize
    #while code>=xmax:
    #    p+="{:b}".format(code%2)
    #    code//=2
    code=(code//symb_fq)*fq_total+cum_freq+(code%symb_fq)
    return code,p
def ransdec_ss(code,cum_freq,symb_fq,fq_total,p):
    code=symb_fq*(code//fq_total)+(code%fq_total)-cum_freq
    #xmax=32
    #renormalize
    #while code < xmax:
    #    code*=2
    #    if len(p)>0:
    #        code+=int(p[-1],2)
    #        p=p[:-1]
    #    else: break
    return code,p

rc_topval=0x00FFFFFF;
rc_botval=0x0000FFFF;
def rcoder_ini():
    low=0;
    rang=0xFFFFFFFF;
    return low,rang
def rcoder_end(low):
    p="{:032b}".format(low)
    return p
def rcenc_ss(low,rang,cum_freq,symb_fq,fq_total): #
    p=""
    rang//=fq_total;
    low+=cum_freq*rang;
    rang*=symb_freq;
    return low,rang,p
def rdecoder_ini(p):
    low=0;
    range=0xFFFFFFFF;
    code=int(p
    return low,range,code,p
def rdecoder_freq():
def ransenc(bs):
    global m
    global rs
    global c
    x=0
    ftot=rs[-1]
    po=""
    print(x,':',po)
    for ss in bs:
        sn=m.index(ss)
        fs=c[ss]
        cf=rs[sn]
        x,p=ransenc_ss(x,cf,fs,ftot)
        print(x,ss,sn,fs,cf,p)
        po+=p
    return "{:b}".format(x)

def rslook(rs,x):
    xmax=32
    m=len(rs)-1
    for v in range(m):
        if (x>=rs[v]) and (x<rs[v+1]):
            return v,rs[v]
    return xmax-1,rs[-1]

def ransdec(pp,cnt):
    global m
    global rs
    global c
    x=int(pp,2)
    #pp=pp[:-45]
    ftot=rs[-1]
    bs=[]
    print(x,":",pp)
    for i in range(cnt):
        snr=x%ftot
        sn,cf=rslook(rs,snr)
        ss=m[sn]
        fs=c[ss]
        bs.insert(0,ss)
        x,pp=ransdec_ss(x,cf,fs,ftot,pp)
        print(x,ss,pp)
    return bs

def testrans():
    tl=0
    tll=0
    ml=0
    nl=100
    for i in range(96):
        s=chr(32+i)
        ss=chr_data(s)
        po=ransenc(ss)
        ls=len(po)
        ml=max(ml,ls)
        nl=min(nl,ls)
        tl+=ls
        tll+=ls*ls
        print(s,ls,po)
    al=tl/96
    print(tl, al, math.sqrt(tll/96-al*al), nl, ml)


def simplenc(bs):
    global m
    dic_sz=24
    x=0
    #print(x,':')
    for ss in bs:
        sn=m.index(ss)
        x=x*dic_sz+sn
        #print(x,ss)
    return "{:b}".format(x)

def simpldec(pp):
    global m
    dic_sz=24
    x=int(pp[-45:],2)
    pp=pp[:-45]
    bs=[]
    print(x,":",pp)
    for i in range(8):
        sn=x%dic_sz
        ss=m[sn]
        bs.insert(0,ss)
        x=x//dic_sz
        #print(x,ss)
    return bs

def testsimpl():
    tl=0
    tll=0
    ml=0
    nl=100
    for i in range(96):
        s=chr(32+i)
        ss=chr_data(s)
        po=simplenc(ss)
        ls=len(po)
        ml=max(ml,ls)
        nl=min(nl,ls)
        tl+=ls
        tll+=ls*ls
        print(s,ls,po)
    al=tl/96
    print(tl, al, math.sqrt(tll/96-al*al), nl, ml)


#
#

print(os.getcwd())

b=readfont("Cbios_8x8.bin")
patchfnt()

c=freqs(b)
#c=freqnib(b)
#c=freqsb(b)
m=symap(c)
#m=symap2(c)
rs,ftot=rangs(m,c)
#print(c)
#c['0']=15
#c['1']=1
prindict(m,c)
#prindict(m,c,full=True)
#print(m)
#prindata(m)
#print(rs,ftot)

#v=b.copy()
#v.sort()
#print(v)

#prinbytein(160)
#
# uniq 40        56       88        208
# uniq $132(4,4) J(266,0) %133(5,4) %69(5,2)
#
# dble 24         104         184         200(3)
# dble < 60(28,1) Q433(273,5) G359(263,3) % 37(5,1)
# dble <188(28,5) a673(513,5) r594(530,2) N(270,0)
# trpl                                    x600(536,2)
#


#huff,dehff=huff45,dehff45     #3205bit avg33.39 stde1.3 32..37 24
#huff,dehff=huff36,dehff36     #3072bit avg32.00 stde4.9 24..42 36
#huff,dehff=huff35,dehff35     #2816bit avg29.33 stde3.3 24..36 20
#huff,dehff=huff346,dehff346   #2826bit avg29.44 stde3.8 24..39 24
huff,dehff=huff246,dehff246   #2668bit avg27.79 stde5.1 16..36 22
#huff,dehff=huff3457,dehff3457 #2819bit avg29.36 stde4.2 24..42 28
#huff,dehff=huff1467,dehff1467 #2717bit avg28.30 stde6.9  8..42 29
#huff,dehff=huff1357,dehff1357 #2658bit avg27.69 stde7.3  8..42 23
#huff,dehff=huff3456,dehff3456 #2756bit avg28.71 stde3.4 24..38 20


ss=chr_data('&')
#ssb=chr_bits('k')
#ssn=chr_nibs('&')
#prindata(ss)
#ps=pakdata(m,ss)
#us=unpdata(m,ps)
#print(ps,len(ps))
#prindata(us)
o=ransenc(ss)
#o=ransenc(ssb)
#o=ransenc(ssn)
#o=simplenc(ss)
print(o,'len',len(o))
r=ransdec(o,8)
#rn=ransdec(o,16)
#rb=ransdec(o,64)
#r=simpldec(o)
#prindata(r)


#testrans2()
#testsimpl()
#testrans()
#testall()
#testhuff(huff,dehff)

#princhr("&")

#prinstr(" !\"#$%&\'")
#prinstr("()*+,-./")
#prinstr("01234567")
#prinstr("89:;<=>?")
#prinstr("@ABCDEFG")
#prinstr("HIJKLMNO")
#prinstr("PQRSTUVW")
#prinstr("XYZ[\\]^_")
#prinstr("`abcdefg")
#prinstr("hijklmno")
#prinstr("pqrstuvw")
#prinstr("xyz{|}~\x7f")

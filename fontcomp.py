import os

print(os.getcwd())

def readfont(n):
    with open(n,"rb") as f:
        b=list(f.read())
        f.close()
    return b
    
def countmap(lst):
    c=[0]*256
    for i in lst: c[i]+=1
    return c

def histomap(lst):
    d={}
    for i in range(256):
        if lst[i]!=0: d[i]=lst[i]
    return d

def chr_i0(a):
    i0=ord(a)-32
    i0=(i0<0) and 0 or (i0>=95 and 0 or i0)
    return 256*(i0//32)+i0%32

def i_chr(i): return chr(32+i%32+32*(i//256))
    
def i_i0(i): return i%32+256*(i//256),(i//32)%8

def prbin(bj): return ("{:08b}".format(bj)).replace("0",".")

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

def chr_data(a):
    global b
    bs=[]
    i0=chr_i0(a)
    for i in range(8):
        bs.append(b[i*32+i0])
    return bs

def prindata(bs):
    for e in bs:
        print("{:08b}".format(e))

# 24 values
def huff45(i):
    if i<8:
        return "{:04b}".format(i+8)
    else:
        return "{:05b}".format(i-8)
def dehff45(s):
    if s[0]=='1':
        return int(s[0:4],2)-8,s[4:]
    else:
        return int(s[0:5],2)+8,s[5:]

# 36 values
def huff36(i):
    if i<4:
        return "{:03b}".format(i+4)
    else:
        return "{:06b}".format(i)
def dehff36(s):
    if s[0]=='1':
        return int(s[0:3],2)-4,s[3:]
    else:
        return int(s[0:6],2),s[6:]

# 20 values
def huff35(i):
    if i<4:
        return "{:03b}".format(i+4)
    else:
        return "{:05b}".format(i-4)
def dehff35(s):
    if s[0]=='1':
        return int(s[0:3],2)-4,s[3:]
    else:
        return int(s[0:5],2)+4,s[5:]

# 24 values
def huff346(i):
    if i<4:
        return "{:03b}".format(i+4)
    elif i<8:
        return "{:04b}".format(i)
    else:
        return "{:06b}".format(i-8)
def dehff346(s):
    if s[0]=='1':
        return int(s[0:3],2)-4,s[3:]
    elif s[1]=='1':
        return int(s[0:4],2),s[4:]
    else:
        return int(s[0:6],2)+8,s[6:]

# 22 values
def huff246(i):
    if i<2:
        return "{:02b}".format(i+2)
    elif i<6:
        return "{:04b}".format(i+2)
    else:
        return "{:06b}".format(i-6)
def dehff246(s):
    if s[0]=='1':
        return int(s[0:2],2)-2,s[2:]
    elif s[1]=='1':
        return int(s[0:4],2)-2,s[4:]
    else:
        return int(s[0:6],2)+6,s[6:]

# 28 values
def huff3457(i):
    if i<4:
        return "{:03b}".format(i+4)
    elif i<8:
        return "{:04b}".format(i)
    elif i<12:
        return "{:05b}".format(i-4)
    else:
        return "{:07b}".format(i-12)
def dehff3457(s):
    if s[0]=='1':
        return int(s[0:3],2)-4,s[3:]
    elif s[1]=='1':
        return int(s[0:4],2),s[4:]
    elif s[2]=='1':
        return int(s[0:5],2)+4,s[5:]
    else:
        return int(s[0:7],2)+12,s[7:]

# 20 values
def huff3456(i):
    if i<4:
        return "{:03b}".format(i+4)
    elif i<8:
        return "{:04b}".format(i)
    elif i<12:
        return "{:05b}".format(i-4)
    else:
        return "{:06b}".format(i-12)
def dehff3456(s):
    if s[0]=='1':
        return int(s[0:3],2)-4,s[3:]
    elif s[1]=='1':
        return int(s[0:4],2),s[4:]
    elif s[2]=='1':
        return int(s[0:5],2)+4,s[5:]
    else:
        return int(s[0:6],2)+12,s[6:]

# 29 values
def huff1467(i):
    if i==0:
        return "1"
    elif i<5:
        return "{:04b}".format(i+3)
    elif i<13:
        return "{:06b}".format(i+3)
    else:
        return "{:07b}".format(i-13)
def dehff1467(s):
    if s[0]=='1':
        return 0,s[1:]
    elif s[1]=='1':
        return int(s[0:4],2)-3,s[4:]
    elif s[2]=='1':
        return int(s[0:6],2)-3,s[6:]
    else:
        return int(s[0:7],2)+13,s[7:]

# 23 values
def huff1357(i):
    if i==0:
        return "1"
    elif i<3:
        return "{:03b}".format(i+1)
    elif i<7:
        return "{:05b}".format(i+1)
    else:
        return "{:07b}".format(i-7)
def dehff1357(s):
    if s[0]=='1':
        return 0,s[1:]
    elif s[1]=='1':
        return int(s[0:3],2)-1,s[3:]
    elif s[2]=='1':
        return int(s[0:5],2)-1,s[5:]
    else:
        return int(s[0:7],2)+7,s[7:]

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

b=readfont("Cbios_8x8.bin")
# patch
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

#v=b.copy()
#v.sort()
c=histomap(countmap(b))
m=sorted(c, key=c.get, reverse=True)

#print(c)
#
# uniq 40        56       88        208
# uniq $132(4,4) J(266,0) %133(5,4) %69(5,2)
#
# dble 24         104         184         200(3)
# dble < 60(28,1) Q433(273,5) G359(263,3) % 37(5,1)
# dble <188(28,5) a673(513,5) r594(530,2) N(270,0)
# trpl                                    x600(536,2)
#
#j=b.index(72)
#print(j,i_chr(j),i_i0(j))
#c.sort()
#print(c)
princhr("&")

for e in m: print(c[e], e)
#print(m)
print('dict:',len(m))

#ss=chr_data('%')
#ps=pakdata(m,ss)
#us=unpdata(m,ps)
#prindata(ss)
#print(ps,len(ps))
#prindata(us)

def testhuff(f,g):
    tl=0
    for i in range(24):
        sq=f(i)
        n2,s=g(sq)
        tl+=len(sq)
        print("{:2}".format(i),"{:2}".format(n2),sq)
    print(tl)

import math

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

#huff,dehff=huff45,dehff45     #3205bit avg33.39 stde1.3 32..37 24
#huff,dehff=huff36,dehff36     #3072bit avg32.00 stde4.9 24..42 36
#huff,dehff=huff35,dehff35     #2816bit avg29.33 stde3.3 24..36 20
huff,dehff=huff346,dehff346   #2826bit avg29.44 stde3.8 24..39 24
#huff,dehff=huff246,dehff246   #2668bit avg27.79 stde5.1 16..36 22
#huff,dehff=huff3457,dehff3457 #2819bit avg29.36 stde4.2 24..42 28
#huff,dehff=huff1467,dehff1467 #2717bit avg28.30 stde6.9  8..42 29
#huff,dehff=huff1357,dehff1357 #2658bit avg27.69 stde7.3  8..42 23
#huff,dehff=huff3456,dehff3456 #2756bit avg28.71 stde3.4 24..38 20

testall()
#testhuff(huff,dehff)

#prinstr("!\"#$%&\'()*")
#prinstr("+,-./:;<=>")
#prinstr("0123456789")
#prinstr("ABCDEFGHIJ")
#prinstr("KLMNOPQRST")
#prinstr("UVWXYZ?@[]")
#prinstr("\\^_`\x7f")
#prinstr("abcdefghij")
#prinstr("klmnopqrst")
#prinstr("uvwxyz{|}~")

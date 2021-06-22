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

def i_chr(i): return chr(32+i%32+32*(i//256))

def i_i0(i): return i%32+256*(i//256),(i//32)%8

def chr_data(a):
    global b
    bs=[]
    for i in range(8):
        bs.append(b[chr_i0(a,i)])
    return bs


def freqs(lst):
    f={}
    for i in lst:
        try: f[i]+=1
        except: f[i]=1
    return f

def freq_scale(a,f):
    fo={}
    for k,fv in a.items():
        fo[k]=int(fv/f)
    return fo

def freq_flat(a,f):
    fo={}
    for k,fv in a.items():
        fo[k]=1
    return fo

def symap(f): return [x for x in f.keys()]
def symapd(f): return sorted(f, key=f.get, reverse=True)
def symapa(f): return sorted(f, key=f.get)

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
    for e in bs: print(prbin(e))

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
    #b[6]-=32
    b[38]-=16
    b[70]-=32
    #b[134]-=8
    #b[166]+=8
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
    #b[302]+=32
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
    b[742]>>=1
#    b[742]-=64
    #t
    b[660]-=8
    #4
    b[20]+=16
    b[52]+=32+16
    b[84]+=64+16
    b[148]+=16
    b[180]+=16
    #[
 #   b[283]>>=1
 #   b[315]>>=1
 #   b[347]>>=1
 #   b[379]>>=1
 #   b[411]>>=1
 #   b[443]>>=1
    #]
    b[285]<<=1
    b[317]<<=1
    b[349]<<=1
    b[381]<<=1
    b[413]<<=1
    b[445]<<=1
    #K
    b[331]+=64
    b[363]-=64+16
    #k
    b[587]-=16
    b[619]-=16
    #@
    b[384]-=16
    b[416]-=16+8+64
    b[448]-=64
    #B
    #b[258]+=16
    #b[290]-=8
    #b[322]+=16
    #b[354]-=8
    #test
    #b[166]=0
    #b[433]=0

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


RANS_L=0x7FFF
def ransenc_ss(code,cum_freq,symb_fq,fq_total): # 
    return (code//symb_fq)*fq_total+cum_freq+(code%symb_fq)
def ransdec_ss(code,cum_freq,symb_fq,fq_total):
    return symb_fq*(code//fq_total)+(code%fq_total)-cum_freq
def ransenc_renorm(code,cf,f,ft,p):
    while True:
        pcode=ransenc_ss(code,cf,f,ft)
        if pcode<2*RANS_L:
            code=pcode
            break
        else:
            p+="{:b}".format(code%2)
            code//=2
    return code,p
def ransdec_renorm(code,p):
    while code<RANS_L and len(p)>0:
        code*=2
        code+=int(p[-1],2)
        p=p[:-1]
    return code,p
def ransenc_fin(code,p):
    p+="{:016b}".format(code)
    return p
def ransdec_begin(p):
    code=int(p[-16:],2)
    return code,p[:-16]


RC_MAXVAL=0xFFFFFFFF
RC_TOPVAL=0x00FFFFFF
RC_BOTVAL=0x0000FFFF
def rc_renormalize(low,rang,top,prec,bot): # top/precitsion/bottom
    while low^(low+rang)<top:
        #get_or_put
        rang<<=prec
        low=(low<<prec)&RC_MAXVAL
    while rang<bot:
        rang=-low & (bot-1)
        #get_or_put
        rang<<=prec
        low=(low<<prec)&RC_MAXVAL
    return low,rang
def re_ss(low,rang,cum_freq,symb_fq,fq_total):
    ob=""
    rang//=fq_total
    low+=cum_freq*rang
    rang*=symb_fq
    #while (low^(low+rang))<RC_TOPVAL or rang<RC_BOTVAL and (rang:=-low&(RC_BOTVAL-1),True):
    #    #ob+="{:b}".format((low>>31)&1)
    #    rang<<=1
    #    low=(low<<1)#&RC_MAXVAL
    low,rang=rc_rc_renormalize(low,rang,RC_TOPVAL,1,RC_BOTVAL)
    return low,rang,ob
def rd_freq(low,rang,fq_total):
    rang//=fq_total
    return low//rang
def rd_ss(low,rang,cum_freq,symb_freq,fq_total):
    rang//=fq_total
    low+=cum_freq*rang
    rang*=symb_freq
    low,rang=rc_renormalize(low,rang,RC_TOPVAL,1,RC_BOTVAL)
    return low,rang

def rcoder_ini():
    low=0
    rang=RC_MAXVAL
    p=""
    return low,rang,p
def rcoder_end(low,p):
    p+="{:032b}".format(low)
    return p
def rcenc_ss(low,rang,cum_freq,symb_fq,fq_total,p):
    rang//=fq_total
    low+=cum_freq*rang
    rang*=symb_fq
    while (low ^ (low+rang))<RC_TOPVAL:
        p+="{:08b}".format(low>>24)
        rang<<=8
        low=(low<<8)&RC_MAXVAL
    while rang < RC_BOTVAL:
        rang=-low&(RC_BOTVAL-1)
        p+="{:08b}".format(low>>24)
        rang<<=8
        low=(low<<8)&RC_MAXVAL
    return low,rang,p
    
def rdecoder_ini(p):
    low=0
    range=RC_MAXVAL
    code=int(p[:32],2)
    return low,rang,code,p[32:]
def rdecoder_freq(low,rang,code,fq_total): # range goes TEMP=rang/fqtotal
    rang//=fq_total
    return rang,(code-low)//rang
def rdec_ss(low,rang,code,cum_freq,symb_freq,p): # range is TEMP
    low+=cum_freq*rang
    rang*=symb_freq
    while (low ^ (low+rang))<RC_TOPVAL:
        code=(code<<8)+int(p[:8],2)
        p=p[8:]
        rang<<=8
        low=(low<<8)&RC_MAXVAL
    while rang < RC_BOTVAL:
        rang=-low&(RC_BOTVAL-1)
        code=(code<<8)+int(p[:8],2)
        p=p[8:]
        rang<<=8
        low=(low<<8)&RC_MAXVAL
    return low,rang,code,p

def rcenc(bs):
    global m
    global rs
    global c
    ftot=rs[-1]
    l,r,po=rcoder_ini()
    for ss in bs:
        sn=m.index(ss)
        fs=c[ss]
        cf=rs[sn]
        l,r,po=rcenc_ss(l,r,cf,fs,ftot,po)
    po=rcoder_end(l,po)
    return po
    
def rce_lr(bs):
    global m
    global rs
    global c
    ftot=rs[-1]
    l,r,p=rcoder_ini()
    print("{:3} {:08x} {:08x}".format("-",l,r))
    for ss in bs:
        sn=m.index(ss)
        fs=c[ss]
        cf=rs[sn]
        l,r,op=re_ss(l,r,cf,fs,ftot)
        print("{:3} {:08x} {:08x} {}".format(sn,l,r,op))
        

def ransenc(bs):
    global m
    global rs
    global c
    p=""
    x=0
    ftot=rs[-1]
    for ss in bs:
        sn=m.index(ss)
        fs=c[ss]
        cf=rs[sn]
        x,p=ransenc_renorm(x,cf,fs,ftot,p)
        #print("{:3} {:5} {}".format(ss,x,p))
    p=ransenc_fin(x,p)
    return p

def rslook(rs,x):
    xmax=32
    m=len(rs)-1
    for v in range(m):
        if (x>=rs[v]) and (x<rs[v+1]):
            return v,rs[v]
    return xmax-1,rs[-1]

def ransdec(pp,cnt=8):
    global m
    global rs
    global c
    ftot=rs[-1]
    bs=[]
    x,p=ransdec_begin(pp)
    #print("{:3} {:5} {}".format("-",x,p))
    for i in range(cnt):
        x,p=ransdec_renorm(x,p)
        snr=x%ftot
        sn,cf=rslook(rs,snr)
        ss=m[sn]
        fs=c[ss]
        bs.insert(0,ss)
        #print("{:3} {:5} {}".format(ss,x,p))
        x=ransdec_ss(x,cf,fs,ftot)
    return bs

def stat(lens):
    nsym=len(lens)
    tl=0
    tll=0
    ml=0
    nl=1e6
    for l in lens:
        tl+=l
        tll+=l*l
        ml=max(ml,l)
        nl=min(nl,l)
    al=tl/nsym
    se=math.sqrt(tll/nsym-al*al)
    print("total:",tl, "average",al, "stderr",se, "min",nl, "max",ml)

def testrans():
    lens=[]
    for i in range(96):
        s=chr(32+i)
        ss=chr_data(s)
        po=ransenc(ss)
        ls=len(po)
        lens.append(ls)
        print(s,ls,po)
    stat(lens)

def testransall():
    global b
    ss=[] #b
    for i in range(96):
        s=chr(32+i)
        ss+=chr_data(s)
    po=ransenc(ss)
    print(len(po),po)
    bs=ransdec(po,8*96)
#    prindata(bs)

#
#

print(os.getcwd())

b=readfont("Cbios_8x8.bin")
patchfnt()

c=freqs(b)
c=freq_scale(c,2.9)
#c=freq_flat(c,0)
#c[0]=5+5
#c[136]=4
#m=symap(c)
m=symapd(c)
#m=symapa(c)
rs,ftot=rangs(m,c)
#print(c)
#prindict(m,c)
prindict(m,c,full=True)
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
# max entrop symbols: $:33 $:43 ):34 3:35 4:36 <:35 >:35
#      @:40 B:41 E:35 F:34 J:33 K:41 L:33 N:36 Q:36 R:36 S:34 ]:35
#      d:33 j:33 k:42 t:36 



#princhr("%")
ss=chr_data('%')
#prindata(ss)
#o=ransenc(ss)
#print(" "*9,o,'len',len(o))
#r=ransdec(o,8)
#prindata(r)

#testrans()
testransall()


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

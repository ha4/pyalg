from ac0 import *

QBLOCKS='\u2594\u2598\u259D\u2580\u2596\u258c\u259e\u259b\u2597\u259A\u2590\u259c\u2584\u2599\u259F\u2588'

def dump_buf(buf):
    w=len(buf)
    h=8
    for h0 in range(0,h,2):
        p=""
        m0=1<<h0
        m1=1<<(h0+1)
        for x0 in range(0,w,2):
            i=(buf[x0]&m0)>>h0
            i+=((buf[x0+1]&m0)>>h0)<<1
            i+=((buf[x0]&m1)>>(h0+1))<<2
            i+=((buf[x0+1]&m1)>>(h0+1))<<3
            p+=QBLOCKS[i]
        print(p)

def set_pixel_8v1(buf,x,y):
    buf[x]|=1<<y

def draw_pixel(fb,x,y):
    adr=x+fb[0]*(y//8)
    m=1<<(y&7)
    buf=fb[7]
    a0=fb[4]
    if adr>=a0 and adr<fb[5]: buf[adr-a0]|=m

def draw_glyph(fb,x,y,bs):
    for l in bs:
        w,q,y=1<<8,x,y+1
        while w:
            if l&w: draw_pixel(fb,q,y-1)
            w,q=w>>1,q+1

def draw_str(fb,x,y,s):
    for c in s:
        draw_glyph(fb,x,y,chr_data(c))
        x+=6

def draw_line(fb,x1,y1,x2,y2):
   a,dx=(x1-x2,-1)if x2<x1 else (x2-x1,1)
   b,dy=(y1-y2,-1)if y2<y1 else (y2-y1,1)
   a2,b2,eps,xcrit=2*a,2*b,0,2*a-b
   while True:
       draw_pixel(fb,x1,y1)
       if x1==x2 and y1==y2: break
       if eps<=xcrit: x1,eps=x1+dx,eps+b2
       if eps>=a or a<=b: y1,eps=y1+dy,eps-a2
           
def draw_circle(fb,x1,y1,r,seg=0xff):
   f=1-r
   ddfx=1
   ddfy=-2*r
   x=0
   y=r
   while x<=y:
        if seg&0x01: draw_pixel(fb,x1+y,y1-x)
        if seg&0x02: draw_pixel(fb,x1+x,y1-y)
        if seg&0x04: draw_pixel(fb,x1-x,y1-y)
        if seg&0x08: draw_pixel(fb,x1-y,y1-x)
        if seg&0x10: draw_pixel(fb,x1-y,y1+x)
        if seg&0x20: draw_pixel(fb,x1-x,y1+y)
        if seg&0x40: draw_pixel(fb,x1+x,y1+y)
        if seg&0x80: draw_pixel(fb,x1+y,y1+x)
        if f>=0:
           y-=1
           ddfy+=2
           f+=ddfy
        x+=1
        ddfx+=2
        f+=ddfx

import tkinter

XYSCALE=4
DISPW=128
DISPH=64

def makecanvas(w=DISPW,h=DISPH):
    global cnv
    cnv=tkinter.Canvas(tkinter.Tk(),width=w*XYSCALE,height=h*XYSCALE)
    cnv.pack()
    cnv.configure(bg='#222')
    return cnv

def write_buf(buf,page=0):
    global cnv
    c="#2dd"
    offs=2
    pg="page{}".format(page)
    d=XYSCALE-1
    x=-XYSCALE+offs
    cnv.delete(pg)
    for b in buf:
        p,x,y=1,x+XYSCALE,page*8*XYSCALE+offs
        while p:
            if b&p: cnv.create_rectangle(x,y,x+d,y+d,outline=c,fill=c,tag=pg)
            p,y=(p<<1)&0xFF,y+XYSCALE

def buf_init(w=DISPW):
    pb=[0]*w
    return pb

def fb_init(h=DISPH,w=DISPW):
    pb=[0]*w
    fb=[w,h, -1,0, 0,0, 0,pb]
    return fb

def fb_page(fb):
    w=fb[0]
    pb=fb[7]
    if fb[2]<0:
        fb[2],fb[3],fb[4],fb[5]=0,0,0,w # page,y0,a0,aend
    else:
        write_buf(pb,fb[2])
        if fb[3]+8>=fb[1]:
            fb[2]=-1
            return False
        else:
            fb[2],fb[3],fb[4],fb[5] = fb[2]+1,fb[3]+8,fb[4]+w,fb[5]+w
    for i in range(len(pb)): pb[i]=0
    return True

def fb_draw():
    global fb
    #draw_line(fb,0,0,DISPW-1,DISPH-1)
    draw_str(fb,17,5,"WelcomE-.012346789")
    draw_str(fb,0,16," !\"#$%&\'()*+,-./")
    draw_str(fb,0,24,"0123456789:;<=>?")
    draw_str(fb,0,32,"@ABCDEFGHIJKLMNO")
    draw_str(fb,0,40,"PQRSTUVWXYZ[\\]^_")
    draw_str(fb,0,48,"`abcdefghijklmno")
    draw_str(fb,0,56,"pqrstuvwxyz{|}~\x7f")
    #draw_circle(fb,32,32,20,255-1)


def test():
    global pb
    pb=buf_init()
    for i in range(8):
        set_pixel_8v1(pb,i,i)
        set_pixel_8v1(pb,8+i,7-i)
        set_pixel_8v1(pb,127-i,i)
        set_pixel_8v1(pb,127-8+i,7)
    dump_buf(pb)

def test_tk():
    global cnv
    global pb
    write_buf(pb,3)

def test_fb():
    global fb
    fb=fb_init()
    while fb_page(fb):
        fb_draw()
    
if __name__ == "__main__":
    test_binload(patch=False)
    #test()
    makecanvas()
    #test_tk()
    test_fb()

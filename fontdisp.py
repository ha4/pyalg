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

def draw_glyph(buf,x,y,bs):
    for l in bs:
        w,q,y=1<<8,x,y+1
        while w:
            if l&w: set_pixel_8v1(buf,q,y-1)
            w,q=w>>1,q+1

def draw_str(buf,x,y,s):
    for c in s:
        draw_glyph(buf,x,y,chr_data(c))
        x+=6

def draw_line(buf,x1,y1,x2,y2):
   a,dx=(x1-x2,-1)if x2<x1 else (x2-x1,1)
   b,dy=(y1-y2,-1)if y2<y1 else (y2-y1,1)
   a2,b2,eps,xcrit=2*a,2*b,0,2*a-b
   while True:
       set_pixel_8v1(buf,x1,y1)
       if x1==x2 and y1==y2: break
       if eps<=xcrit: x1,eps=x1+dx,eps+b2
       if eps>=a or a<=b: y1,eps=y1+dy,eps-a2
           

def buf_init(w=128):
    pb=[0]*w
    return pb

def test():
    global pb
    pb=buf_init()
    for i in range(8):
        set_pixel_8v1(pb,i,i)
        set_pixel_8v1(pb,8+i,7-i)
        set_pixel_8v1(pb,127-i,i)
        set_pixel_8v1(pb,127-8+i,7)
    draw_str(pb,17,0,"WelcomE-.012346789")
    draw_line(pb,1,1,30,5)
    dump_buf(pb)

import tkinter

XYSCALE=4
def makecanvas(w=128,h=32):
    global cnv
    cnv=tkinter.Canvas(tkinter.Tk(),width=w*XYSCALE,height=h*XYSCALE)
    cnv.pack()
    cnv.configure(bg='#222')
    return cnv

def plotbuf(buf,page=0):
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


def test_tk():
    global cnv
    global pb
    plotbuf(pb,0)
    plotbuf(pb,3)
    #cnv.create_rectangle(0,0,0+1,0+1,outline='#fff')

if __name__ == "__main__":
    test_binload()
    test()
    makecanvas()
    test_tk()

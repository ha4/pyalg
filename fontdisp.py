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
        x+=8

def buf_init(w=128):
    global pb
    pb=[0]*w

def test():
    global pb
    buf_init()
    for i in range(8):
        set_pixel_8v1(pb,i,i)
        set_pixel_8v1(pb,8+i,7-i)
        set_pixel_8v1(pb,127-i,i)
        set_pixel_8v1(pb,127-8+i,7)
    draw_str(pb,17,0,"welcom")
    dump_buf(pb)


if __name__ == "__main__":
    test_binload()
    test()

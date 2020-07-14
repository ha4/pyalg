class mazebrd:
    """
    Maze border list.
    directions:
      1_
    0 | | 2
      3^ 
    """
    def __init__(self,size,ysize=None):
        self.hsize=size
        self.vsize=size if ysize==None else ysize
        self.h=[False]*(self.vsize*(self.hsize+1))
        self.v=[False]*(self.hsize*(self.vsize+1))
    def map(self,x,y,xsz):
        return x+y*(xsz+1)
    def wall(self,x,y,dir):
        if dir&1:
            self.v[self.map(y,x,self.vsize)+(dir >> 1)]=True
        else:
            self.h[self.map(x,y,self.hsize)+(dir >> 1)]=True
    def iswall(self,x,y,dir):
        if dir&1:
            return self.v[self.map(y,x,self.vsize)+(dir >> 1)]
        else:
            return self.h[self.map(x,y,self.hsize)+(dir >> 1)]
    def empty(self):
        for m in range(self.vsize):
            self.h[m]=False
            self.v[m]=False
        m=self.hsize
        for n in range(self.vsize):
            v=self.map(0,n,self.hsize)
            self.h[v]=True
            self.h[v+m]=True
        m=self.vsize
        for n in range(self.hsize):
            v=self.map(0,n,self.vsize)
            self.v[v]=True
            self.v[v+m]=True

def dumpmaze(m):
    # first line
    for x in range(m.hsize):
        print(' ','_' if m.iswall(x,0,1) else ' ',sep='',end='')
    print()
    # other line
    for y in range(m.vsize):
        for x in range(m.hsize):
            print('|' if m.iswall(x,y,0) else ' ',
                  '_' if m.iswall(x,y,3) else ' ',
                  sep='',end='')
        print('|' if m.iswall(x,y,2) else ' ')

import tkinter
cnv=0
def makecanvas():
    global cnv
    cnv=tkinter.Canvas(tkinter.Tk(),width=528,height=400)
    cnv.pack()
    return cnv

def plotmaze(m,cellsz=16):
    for y in range(m.vsize):
        for x in range(m.hsize):
            xp,xn=cellsz/2+x*cellsz,cellsz/2+(x+1)*cellsz
            yp,yn=cellsz/2+y*cellsz,cellsz/2+(y+1)*cellsz
            if x==0 and m.iswall(x,y,0):
                cnv.create_line(xp,yp,xp,yn,width=2)
            if y==0 and m.iswall(x,y,1):
                cnv.create_line(xp,yp,xn,yp,width=2)
            if m.iswall(x,y,2):
                cnv.create_line(xn,yp,xn,yn,width=2)
            if m.iswall(x,y,3):
                cnv.create_line(xp,yn,xn,yn,width=2)

import random

xdens=0.5
ydens=0.5
rnx=0
rny=0

def xrand():
    global rnx,xdens
    rnx+=1
    return random.random() <= xdens
def yrand():
    global rny,ydens
    rny+=1
    return random.random() <= ydens

def makeuniq(s):
    n=len(s)
    st=set(range(n))
    st.difference_update(s)
    for x in range(n):
        if s[x]<0: s[x]=st.pop()

def mergeh(s,m,y):
    for x in range(len(s)-1):
        if s[x]!=s[x+1]:
            if xrand(): m.wall(x,y,2)
            else: s[x+1]=s[x]
        else:
            m.wall(x,y,2)

def mergeh0(s,m,y):
    for x in range(len(s)-1):
        if s[x]!=s[x+1]:
            if xrand(): pass
            else: s[x+1]=s[x]
        else:
            m.wall(x,y,2)

def mergev(s,m,y):
    lim=len(s)
    def slen(x,t,n=0):
        while x < lim and s[x]==t:
            x+=1
            n+=1
        return n
    i=0
    while i < lim:
        n=slen(i,s[i])
        k=1
        for x in range(i,i+n):
            if n>k and yrand():
                s[x]=-1
                m.wall(x,y,3)
                k+=1
        i+=n

def makemaze(m):
    s=[-1]*m.hsize
    for y in range(m.vsize-1):
        makeuniq(s)
        mergeh(s,m,y)
        mergev(s,m,y)
    makeuniq(s)
    mergeh0(s,m,m.vsize-1)

m1=mazebrd(32,24)
m1.empty()
makemaze(m1)
print("rnx:",rnx,"rny:",rny,"sum:",rnx+rny)
# dumpmaze(m1)
makecanvas()
plotmaze(m1)

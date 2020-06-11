class mazebrd:
    """
    Maze border list.
    directions:
      1_
    0 | | 2
      3^ 
    """
    def __init__(self,size):
        self.size=size
        self.vsize=size*(size+1)
        self.h=[False]*(self.vsize)
        self.v=[False]*(self.vsize)
    def map(self,x,y):
        return x+y*(self.size+1)
    def wall(self,x,y,dir):
        if dir&1:
            self.v[self.map(y,x)+(dir >> 1)]=True
        else:
            self.h[self.map(x,y)+(dir >> 1)]=True
    def iswall(self,x,y,dir):
        if dir&1:
            return self.v[self.map(y,x)+(dir >> 1)]
        else:
            return self.h[self.map(x,y)+(dir >> 1)]
    def empty(self):
        for m in range(self.vsize):
            self.h[m]=False
            self.v[m]=False
        m=self.size
        for n in range(self.size):
            v=self.map(0,n)
            self.h[v]=True
            self.h[v+m]=True
            self.v[v]=True
            self.v[v+m]=True

def dumpmaze(m):
    n=m.size;
    # first line
    for x in range(n):
        print(' ','_' if m.iswall(x,0,1) else ' ',sep='',end='')
    print()
    # other line
    for y in range(n):
        for x in range(n):
            print('|' if m.iswall(x,y,0) else ' ',
                  '_' if m.iswall(x,y,3) else ' ',
                  sep='',end='')
        print('|' if m.iswall(x,y,2) else ' ')

import tkinter
cnv=0
def makecanvas():
    global cnv
    cnv=tkinter.Canvas(tkinter.Tk(),width=500,height=400)
    cnv.pack()
    return cnv

def plotmaze(m,cellsz=16):
    n=m.size;
    for y in range(n):
        for x in range(n):
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

def makeuniq(s):
    n=len(s)
    st=0
    for i in range(n):
        if s[i]<0:
            s[i]=st
            st+=1
        else:
            st=s[i]
    
def makeline(m):
    s=[-1]*m.size
    makeuniq(s)
    print(s)

m1=mazebrd(8)
m1.empty()
m1.wall(1,1,0)
m1.wall(1,1,1)
m1.wall(1,2,2)
m1.wall(1,1,3)
makeline(m1)

dumpmaze(m1)
makecanvas()
plotmaze(m1)

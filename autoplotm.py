import tkinter
from math import floor,ceil,log10,pow

class AutoPlot:

    def masaxis(self, dmin, dmax):
        if dmax>dmin:
            ords=floor(log10(dmax-dmin))
        elif dmax==dmin and dmax!=0:
            ords=floor(log10(abs(dmax)))
        else:
            return None
        ddd=pow(10,ords-1)
        ord2=ceil((dmax-dmin)/ddd)
        astp=ddd*(1 if ord2<10 else 2 if ord2<20 else 5 if ord2<50 else 10)
        amin=astp*floor(dmin/astp)
        amax=astp*ceil(dmax/astp)
        return (amin,amax,astp)

    def scaler(self, dmin, dmax, pixels):
        a=1 if dmin==dmax else pixels/(dmax-dmin)
        b=-dmin*a-(pixels if pixels<0 else 0)
        return (b,a)

    def pix(self,ab,coord):
        b,a=ab
        return int(a*coord+b)

    def unpix(self,axis,pixel):
        try: b,a=self.scale[axis,"ab"]
        except: return pixel
        return (pixel-b)/a

    def limits(self,axis):
        try: mi,ma=self.scale[axis,"amin"],self.scale[axis,"amax"]
        except: return 0,0
        return mi,ma

    def rescaler(self,name,nscale):
        nb,na=nscale
        try:
            b,a=self.scale[name,"ab"]
            s=na/a
            o=(b-nb) if s==1 else ((b*s-nb)/(s-1))
            rc=(o,s)
        except: rc=(0,1)
        self.scale[name,"ab"]=nscale
        return rc

    def drawaxis(self,sel,size,fixed,atg):
        p=self.pscale
        ta={"tag":atg}
        ga={"dash":(2,2), **ta}
        if (atg,"gcolor") in p: ga.update({"fill":p[atg,"gcolor"]})
        if (atg,"tcolor") in p: ta.update({"fill":p[atg,"tcolor"]})
        if (atg,"anchor") in p: ta.update({"anchor":p[atg,"anchor"]})
        if (atg,"offset") in p: fixed+=p[atg,"offset"]
        d=self.scale[atg,"astep"]
        e=self.scale[atg,"amax"]+0.5*d
        v=self.scale[atg,"amin"]
        ab=self.scale[atg,"ab"]
        while v<e:
            vp=self.pix(ab,v)
            x,y=[vp,fixed,vp][sel:sel+2]
            try: atxt=p[atg,"fmt"].format(v)
            except: atxt=str(v)
            x0,y0=[x,0,y][sel:sel+2]
            x1,y1=[x,size,y][sel:sel+2]
            self.canvas.create_line(x0,y0,x1,y1,**ga)
            self.canvas.create_text(x+3,y-3,text=atxt,**ta)
            v+=d

    def getdset(self,a,t): return set([k[0] for k,v in self.dset.items() if k[1]==a and v==t])

    def replot(self,atg="all"):
        if atg=="all":
            for v in set([k[0] for k in self.scale.keys() if k[1]=="ab"]):
                self.replot(atg=v)
            return
        try:
            p,q,r=self.masaxis(self.scale[atg,"vmin"],self.scale[atg,"vmax"])
            self.scale.update({(atg,"amin"):p, (atg,"amax"):q, (atg,"astep"):r})
        except:
            return
        slst=self.getdset("xaxis",atg)
        if len(slst)>0:
            sel=0
        else:
            slst=self.getdset("yaxis",atg)
            if len(slst)>0:
                sel=1
            else:
                return
        ww,wh=self.canvas.winfo_width(),self.canvas.winfo_height()
        pix=-wh if sel==1 else ww
        tmp=self.scaler(self.scale[atg,"amin"],self.scale[atg,"amax"],pix)
        mv,sc=self.rescaler(atg,tmp)
        if mv==0 and sc==1:
            return
        self.canvas.delete(atg)
        for s in slst:
            xs,ys=[sc,1,sc][sel:sel+2]
            xo,yo=[mv,0,mv][sel:sel+2]
            self.canvas.scale(s,xo,yo,xs,ys)
        h,h0=(ww,0) if sel==1 else (wh,wh)
        self.drawaxis(sel,h,h0,atg)
        self.canvas.tag_lower(atg)

    def createaxis(self,xy,dtg="set1",fmt="{:5g}",anchor="w"):
        if xy[0]=="x":
            a="xaxis"
        elif xy[0]=="y":
            a="yaxis"
        else:
            return
        self.dset[dtg,a]=xy
        self.pscale.update({(xy,"fmt"):fmt, (xy,"anchor"):anchor,
                            (xy,"tcolor"):"black", (xy,"gcolor"):"darkgray"})

    def doresize(self,evt):
        try:
            self.canvas.after_cancel(self._job)
            self._job=None
        except: pass
        self._job=self.canvas.after(50, self.replot)

    def clear(self):
        self.canvas.delete(tkinter.ALL)
        self.lastpt={}
        self.scale={}
        self.canvas.bind('<Configure>',self.doresize)

    def cleantag(self,tg):
        self.canvas.delete(tg)
        self.lastpt[tg]=None

    def plotXYdot(self,x,y,t,c,xs,ys):
        px,py=self.pix(xs,x),self.pix(ys,y)
        self.canvas.create_line(px,py-1,px,py+1,fill=c,tag=t)
        self.canvas.create_line(px-1,py,px+1,py,fill=c,tag=t)

    def plotXYline(self,x,y,t,c,xs,ys):
        try: pre=self.lastpt[t]
        except: return
        xp,yp=self.pix(xs,pre[0]),self.pix(ys,pre[1])
        px,py=self.pix(xs,x),self.pix(ys,y)
        self.canvas.create_line(xp,yp,px,py,fill=c,tag=t)

    def plotXYmove(self,x,y,t,c,xs,ys): pass

    def minmax(self,v,n,mi,ma):
        sc=self.scale
        if not((n,mi) in sc and (n,ma) in sc):
            sc[n,mi]=v
            sc[n,ma]=v
            return True
        if v>sc[n,ma]:
            sc[n,ma]=v
            return True
        if v<sc[n,mi]:
            sc[n,mi]=v
            return True
        return False

    def __call__(self, x, y, dtg="set1", typ="line"):
        ds=self.dset
        try: xn=ds[dtg,"xaxis"]
        except: ds[dtg,"xaxis"]=xn="x"
        try: yn=ds[dtg,"yaxis"]
        except: ds[dtg,"yaxis"]=yn="y"
        c=ds[dtg,"color"] if (dtg,"color") in ds else "black"
        self.minmax(x,xn,"vmin","vmax")
        if self.minmax(x,xn,"amin","amax"): self.replot(atg=xn)
        self.minmax(y,yn,"vmin","vmax")
        if self.minmax(y,yn,"amin","amax"): self.replot(atg=yn)
        try: self.ptyp[typ](x,y,dtg,c,self.scale[xn,"ab"],self.scale[yn,"ab"])
        except: pass
        self.lastpt[dtg]=(x,y)

    def __init__(self, c):
        self.canvas=c
        self.scale={}
        self.pscale={}
        self.dset={}
        self.lastpt={}
        self.ptyp={"dot":self.plotXYdot, "line":self.plotXYline, "move":self.plotXYmove}
        
        self.clear()
        self.createaxis("x",anchor="s")
        self.createaxis("y")

def test():
    import random
    import math
    global n,m,rn
    n=10
    z=100
    m=[0]*z
    rn=None
    def nrand():
        global rn
        if not (rn is None):
            r,rn=rn,None
            return r
        while True:
            u=random.randint(-10000,10000)/10000
            v=random.randint(-10000,10000)/10000
            r=u*u+v*v
            if r>0 and r<=1:
                d=(-2*math.log(r)/r)**.5
                rn=v*d
                return u*d
    def selftest():
        global n
        graph(n,n/50+nrand())
        graph(n,n/50,"set2")
        n+=1
        root.after(100,selftest)
    def selftest2():
        global m
        p=z//2+int(z*nrand()/4)
        if p>=0 and p<z:
            m[p]+=1
        graph.cleantag("set1")
        for i in range(z):
            graph(i,m[i])
        root.after(10,selftest2)
    root=tkinter.Tk()
    canvas=tkinter.Canvas(root,width=600,height=500,background="white")
    canvas.pack(fill=tkinter.BOTH,side=tkinter.TOP,expand=True,padx=4,pady=4)
    graph=AutoPlot(canvas)
    graph.dset["set1","color"]="red"
    root.update()
    graph(0,1.2)
    graph(5,1.5)
    graph(8.1,1.414)
    selftest()
    root.mainloop()


if __name__ == "__main__":
    test()

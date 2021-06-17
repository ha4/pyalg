import tkinter
cnv=0
def makecanvas():
    global cnv
    cnv=tkinter.Canvas(tkinter.Tk(),width=528,height=400)
    cnv.pack()
    return cnv


def plotvec(m):
    for c in m:
        p1=c[0]
        p2=c[1]
        cnv.create_line(p1[0],p1[1],p2[0],p2[1],width=2)

def makescene(pov,direction,fov,p):
    pv=pov
    pe=[pov[0]+direction[0], pov[1]+direction[1]]
    rsy=[pv,pe]
    z=p.copy()
    z.append(rsy)
    print(p)
    print(z)
    return z

def makepoly():
    return [[[10, 10], [500, 100]]]

p1=makepoly()
s1=makescene([100, 100], [0, 10], 30, p1)

makecanvas()
plotvec(s1)

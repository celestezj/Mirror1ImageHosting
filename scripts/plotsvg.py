#encoding:utf-8
'''
A demo that use turtle to plot svg image(can be generated by <Vector Magic>).
See info in https://github.com/muggledy/myworld/blob/v0.2/apps/readme.md
Author: muggledy
Date: 2019/10/31
'''

import turtle as tr
from lxml import etree
import os.path
from queue import Queue
import re

__all__=['plotsvg']

svgtag=re.compile(r'(path|rect|circle|ellipse|line|polyline)')
pathcmd=re.compile(r'((M|m|L|l|S|s|Q|q|T|t|H|h|V|v|C|c|A|a|Z)([ ,]*-?\d+\.?\d*[ ,]*)*)')
inthw=re.compile(r'\d+')
steps=5
filllock=False
fillstate=False
stroke=False
ifprint=True
accelerate=None
startpoint=(0,0)
lastbessel=None
csqt=None

def moveto(x,y,rel=False):
    global startpoint
    if rel:
        x+=tr.xcor()
        y+=(-tr.ycor())
    tr.up()
    tr.goto(x,-y)
    tr.down()
    startpoint=(x,y)
    
def hormove(dis,rel=False):
    if rel:
        dis+=tr.xcor()
    tr.setx(dis)

def vermove(dis,rel=False):
    if rel:
        dis+=(-tr.ycor())
    tr.sety(-dis)

def lineto(x,y,rel=False):
    if rel:
        x+=tr.xcor()
        y+=(-tr.ycor())
    tr.goto(x,-y)

def linspace(x0,y0,x1,y1):
    d=(abs(x1-x0)+abs(y1-y0))*2
    n=int(d/steps)
    if n==0:
        return [1]
    j=1/n
    return (i*j for i in range(1,n+1))

def bessel1(p1,p2,t):
    return ((1-t)*p1[0]+t*p2[0],(1-t)*p1[1]+t*p2[1])

def bessel2(x1,y1,x2,y2,rel=False):
    global lastbessel
    x0,y0=tr.pos()
    y0=-y0
    if rel:
        x1+=x0
        y1+=y0
        x2+=x0
        y2+=y0
    lastbessel=[(x1,y1),(x2,y2)]
    for t in linspace(x0,y0,x2,y2):
        T1=bessel1((x0,y0),(x1,y1),t)
        T2=bessel1((x1,y1),(x2,y2),t)
        T=bessel1(T1,T2,t)
        lineto(*T)

def bessel3(x1,y1,x2,y2,x3,y3,rel=False):
    global lastbessel
    x0,y0=tr.pos()
    y0=-y0
    if rel:
        x1+=x0
        y1+=y0
        x2+=x0
        y2+=y0
        x3+=x0
        y3+=y0
    lastbessel=[(x2,y2),(x3,y3)]
    for t in linspace(x0,y0,x3,y3):
        T1=bessel1((x0,y0),(x1,y1),t)
        T2=bessel1((x1,y1),(x2,y2),t)
        T3=bessel1((x2,y2),(x3,y3),t)
        T21=bessel1(T1,T2,t)
        T22=bessel1(T2,T3,t)
        T=bessel1(T21,T22,t)
        lineto(*T)

def symmetricpoint(pos,center):
    return (2*center[0]-pos[0],2*center[1]-pos[1])

def close():
    lineto(*startpoint)

def command(flag,*args,**kwargs):
    global fillstate,lastbessel,csqt
    if ifprint:
        print('    ',flag,args)
    if flag in 'MmLlHhVvAaZ':
        csqt=None
    if flag=='M':
        if filllock:
            if fillstate:
                tr.end_fill()
                tr.begin_fill()
            else:
                tr.begin_fill()
                fillstate=True
        moveto(*args)
    elif flag=='m':
        if filllock:
            if fillstate:
                tr.end_fill()
                tr.begin_fill()
            else:
                tr.begin_fill()
                fillstate=True
        moveto(*args,True)
    elif flag=='L':
        lineto(*args)
    elif flag=='l':
        lineto(*args,True)
    elif flag=='C':
        csqt=='c'
        bessel3(*args)
    elif flag=='c':
        csqt=='c'
        bessel3(*args,True)
    elif flag=='Z':
        close()
        if filllock:
            tr.end_fill()
            fillstate=False
    elif flag=='H':
        hormove(args[0])
    elif flag=='h':
        hormove(args[0],True)
    elif flag=='V':
        vermove(args[0])
    elif flag=='v':
        vermove(args[0],True)
    elif flag=='Q':
        csqt='q'
        bessel2(*args)
    elif flag=='q':
        csqt='q'
        bessel2(*args,True)
    elif flag=='S':
        if csqt=='s' or csqt=='c':
            bessel3(*symmetricpoint(*lastbessel),*args)
        else:
            bessel2(*args)
        csqt='s'
    elif flag=='s':
        if csqt=='s' or csqt=='c':
            p11,p12=symmetricpoint(*lastbessel)
            p21,p22=tr.pos()
            p22=-p22
            bessel3(p11-p21,p12-p22,*args,True)
        else:
            bessel2(*args,True)
        csqt='s'
    elif flag=='T':
        if csqt=='t' or csqt=='q':
            bessel2(*symmetricpoint(*lastbessel),*args)
        else:
            lineto(*args)
        csqt='t'
    elif flag=='t':
        if csqt=='t' or csqt=='q':
            p11,p12=symmetricpoint(*lastbessel)
            p21,p22=tr.pos()
            p22=-p22
            bessel2(p11-p21,p12-p22,*args,True)
        else:
            lineto(*args,True)
        csqt='t'
    elif flag=='A': #No need to write~
        pass
    elif flag=='a':
        pass

def process(node):
    global filllock
    tag=svgtag.search(node.tag)
    if tag:
        tag=tag.group()
        if ifprint:
            print(tag)
        if tag=='path':
            d=node.attrib['d']
            pencolor=node.attrib.get('stroke')
            fillcolor=node.attrib.get('fill')
            if pencolor:
                oldpencolor=tr.pencolor()
                tr.pencolor(pencolor)
            if fillcolor!=None and fillcolor!='none':
                filllock=True
                tr.fillcolor(fillcolor)
                if not stroke:
                    tr.pencolor(fillcolor)
            else:
                filllock=False
            for cmd in pathcmd.findall(d):
                command(cmd[1],*[float(i) for i in re.split('[ ,]+',cmd[0][1:].strip()) if i!=''])
            if pencolor:
                tr.pencolor(oldpencolor)
        elif tag=='rect': #No need to write~
            pass
        elif tag=='circle':
            pass
        elif tag=='ellipse':
            pass
        elif tag=='line':
            pass
        elif tag=='polyline':
            pass
    return

def dtraverse(node):
    process(node)
    if len(node)==0:
        return
    for child in node:
        dtraverse(child)

def btraverse(node):
    q=Queue()
    q.put(node)
    while not q.empty():
        t=q.get()
        process(t)
        if len(t)>0:
            for i in t:
                q.put(i)

def plotsvg(filename,_stroke=False,_steps=10,_accelerate=2,_ifprint=False,_db='d',_signature=None):
    '''The main plotting function.
       _stroke: Drawing stroke with black line.
       _steps: A float(↓) to control the smoothness(↑) of curve, also the drawing speed may be slower if too small.
       _accelerate: Accelerate to plot.
       _ifprint: If print information in console when plotting.
       _db: Deep traversal or breadth traversal the XML tree of svg.
       _signature: A string that you want to signature at the lower right corner.
    '''
    global stroke,steps,accelerate,ifprint
    stroke,steps,accelerate,ifprint=_stroke,_steps,_accelerate,_ifprint
    et=etree.parse(filename)
    svgnode=et.xpath('//*[name()="svg"]')[0]
    h,w=svgnode.attrib.get('height'),svgnode.attrib.get('width')
    h,w=int(inthw.search(h).group()),int(inthw.search(w).group())
    tr.setup(height=h,width=w)
    tr.setworldcoordinates(0,-h,w,0)
    tr.shape(name='circle')
    tr.listen()
    if accelerate!=None:
        tr.tracer(n=accelerate)
    if _db=='d':
        dtraverse(et.getroot())
    elif _db=='b':
        btraverse(et.getroot())
    if _signature is not None:
        tr.pencolor('black')
        moveto(w-40,h-20)
        tr.write(_signature,align="center",font=("Roboto",10,"normal"))
        moveto(w-45,h-15)
        command('l',20,-4)
        moveto(w-38,h-10)
        command('l',10,-4)
    tr.hideturtle()
    tr.update()
    tr.done()

if __name__=='__main__':
    cwd=os.path.dirname(os.path.realpath(__file__))
    svgfile=os.path.join(cwd,'../temp/imgs/nannan.svg')
    plotsvg(svgfile,_accelerate=400,_signature='muggledy')
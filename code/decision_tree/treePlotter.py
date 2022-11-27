'''
Created on Feb 23, 2022
https://webstack.muggledy.top/posts/plotdicttree/
@author: muggledy
'''
import matplotlib.pyplot as plt
import numpy as np

def analysetree(tree,treeanalysis,depth=0,ifprint=False,father='ROOT'):
    if ifprint:
        print('depth:',depth,'\n#\nfather:',father)
    if not isinstance(tree,dict):
        if ifprint:
            print('leaf node:',tree,'\n#')
        treeanalysis['__leaves']=1
        treeanalysis['__leave']=tree
        return 1,depth
    treename=list(tree.keys())[0]
    branches=list(tree[treename].keys())
    treeanalysis[treename]={}
    leaves=0
    maxdepth=[]
    if ifprint:
        print('root node of current subtree:',treename,'\nbranches of the root node:',branches,'\nbranch info:')
        for branch in branches:
            print('    ',branch,':',tree[treename][branch])
        print('#')
    for branch in branches:
        treeanalysis[treename][branch]={}
        t=analysetree(tree[treename][branch],treeanalysis[treename][branch],depth+1,ifprint,treename)
        leaves+=t[0]
        maxdepth.append(t[1])
    treeanalysis[treename]['__leaves']=leaves
    return leaves,max(maxdepth)

def calcposition(tree,depth,wh=(2,1)):
    def f(tree,treeposanalysis,currdepth,xbounds):
        if '__leave' in tree.keys():
            treeposanalysis['__leave']=tree['__leave']
            return
        treename=list(tree.keys())[0]
        branches=list(tree[treename].keys())
        leavenums=tree[treename]['__leaves']
        y=vincrease*currdepth
        subleavenums=[]
        subleavenames=[]
        subleavexbounds=[]
        subleavebranchs=[]
        treeposanalysis[treename]={}
        for branch in branches:
            if branch!='__leaves':
                if tree[treename][branch].get('__leave')!=None:
                    subleavenums.append(tree[treename][branch]['__leaves'])
                    subleavenames.append(tree[treename][branch]['__leave'])
                else:
                    for key in tree[treename][branch].keys():
                        subleavenums.append(tree[treename][branch][key]['__leaves'])
                        subleavenames.append(list(tree[treename][branch].keys())[0])
                subleavebranchs.append(branch)
                treeposanalysis[treename][branch]={}
                
        treeposanalysis[treename]['__pos']=(sum(xbounds)/2,y)
        scale=(xbounds[1]-xbounds[0])/leavenums
        start=xbounds[0]
        for i,e in enumerate(subleavenames):
            t=start+subleavenums[i]*scale
            subleavexbounds.append((start,t))
            start=t
        temp={}
        for i,j,k in zip(subleavenames,subleavexbounds,subleavebranchs):
            temp[str(k)+'_'+str(i)]=j
        
        for branch in branches:
            if branch!='__leaves':
                treeposanalysis[treename][branch]={}
                if len(tree[treename][branch])==2:
                    name=tree[treename][branch]['__leave']
                    treeposanalysis[treename][branch]['__pos']=(sum(temp[str(branch)+'_'+str(name)])/2,y+vincrease)
                else:
                    name=list(tree[treename][branch].keys())[0]
                f(tree[treename][branch],treeposanalysis[treename][branch],currdepth+1,temp[str(branch)+'_'+str(name)])
    vincrease=-wh[1]/depth
    treeposanalysis={}
    f(tree,treeposanalysis,0,(0-wh[0]/2,0+wh[0]/2))
    return treeposanalysis

def plotarrownode(text,front,rear,nodetype=dict(boxstyle='square',facecolor='gray'),arrowtype=dict(arrowstyle='<|-',alpha=0.5)):
    plt.annotate(text,front,rear,arrowprops=arrowtype,bbox=nodetype)

def plotthetree(tree,wh=None,title=None,axis=False,delay=0):
    notleafnode=dict(boxstyle='square',fc='green',alpha=0.6)
    leafnode=dict(boxstyle='round4',facecolor='pink',alpha=0.8)
    if wh!=None:
        plt.axis([-wh[0]/2*(4/3),wh[0]/2*(5/4),-wh[1]*(4/3),0+wh[1]*0.25])
    if not axis:
        ax=plt.gca()
        ax.spines['bottom'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.xticks([])
        plt.yticks([])
    if title!=None:
        plt.title(title,bbox=dict(boxstyle='Roundtooth',alpha=0.4,facecolor='gray'),color='red',size=16)
    flag=True
    def plottree(tree):
        treename=list(tree.keys())[0]
        branches=list(tree[treename].keys())
        treepos=tree[treename]['__pos']
        childpos=None
        nonlocal flag
        if flag:
            flag=False
            plt.text(0,0,treename,ha="center",va="center",size=15,bbox=notleafnode)
        for branch in branches:
            if branch!='__pos':
                if tree[treename][branch].get('__leave')!=None:
                    childpos=leafpos=tree[treename][branch].get('__pos')
                    leafname=tree[treename][branch].get('__leave')
                    plotarrownode(leafname,treepos,leafpos,leafnode)
                    if delay:
                        plt.pause(delay)
                else:
                    childpos=subtreepos=tree[treename][branch][list(tree[treename][branch].keys())[0]]['__pos']
                    subtreename=list(tree[treename][branch].keys())[0]
                    plotarrownode(subtreename,treepos,subtreepos,notleafnode)
                    if delay:
                        plt.pause(delay)
                    plottree(tree[treename][branch])
                plt.annotate('{0}'.format(branch),((treepos[0]+childpos[0])/2,(treepos[1]+childpos[1])/2),rotation=0,bbox=dict(boxstyle='round',facecolor='gray',alpha=0.2))
    plottree(tree)
    plt.show()

def main(treeinfo,title):
    treeanalysis={}
    ret=analysetree(treeinfo,treeanalysis,ifprint=False)
    postree=calcposition(treeanalysis,ret[1],wh=(2,2))
    plotthetree(postree,(1.5,2),title=title,delay=0)
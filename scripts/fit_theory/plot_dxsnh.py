import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import Normalize
import numpy as np
from sympy import *

dots=[(25,110),(27,115),(31,155),(33,160),(35,180)]
X,Y=zip(*dots)

f=lambda x: 7.2*x-73

x=np.linspace(24,36,100)

plt.scatter(X,Y,color='r')
plt.plot(x,f(x),linestyle='--',color='grey',alpha=0.3,label='f(x)=7.2x-73')

'''以多项式函数f(x)=ax^2+bx+c为例进行说明，如何比较快地解下面的三元一次方程组（使用Sympy模块，之所以说比较快而不是很快，因为我之前只看了Sympy教程的快速开始部分，而我下面的方法在高手面前可能显得有点不值一提了）：
∂(ε)/∂(a)=2·∑(a·xi^2+b·xi+c-yi)·xi^2=0
∂(ε)/∂(b)=2·∑(a·xi^2+b·xi+c-yi)·xi  =0
∂(ε)/∂(c)=2·∑(a·xi^2+b·xi+c-yi)     =0
由于数据点的值很大，手动计算十分吃力，容易出错，所以使用Sympy的自动化简功能：
譬如对于∂(ε)/∂(a)，我们在交互模式下输入：25**2*(a*25**2+b*25+c-110) + 27**2*(a*27**2+b*27+c-115) + 31**2*(a*31**2+b*31+c-155) + 33**2*(a*33**2+b*33+c-160) + 35**2*(a*35**2+b*35+c-180)，回车，立即可得：4532133*a + 143911*b + 4629*c - 696280
要输入那么一长串的代码实在吃不消，但是Sympy支持将字符串转换为表达式并进行化简，于是我们只要拼凑出字符串"25**2*(a*25**2+b*25+c-110) + 27**2*(a*27**2+b*27+c-115) + 31**2*(a*31**2+b*31+c-155) + 33**2*(a*33**2+b*33+c-160) + 35**2*(a*35**2+b*35+c-180)"即可：
>>> '+'.join(['{0}**2*(a*{0}**2+b*{0}+c-{1})'.format(*d) for d in dots])
'25**2*(a*25**2+b*25+c-110)+27**2*(a*27**2+b*27+c-115)+31**2*(a*31**2+b*31+c-155)+33**2*(a*33**2+b*33+c-160)+35**2*(a*35**2+b*35+c-180)'
>>> simplify(_)
4532133*a + 143911*b + 4629*c - 696280
同理可求∂(ε)/∂(b)、∂(ε)/∂(c)。最后使用solve解方程组，得到精确解
'''
a,b,c,d,e,f=symbols('a,b,c,d,e,f')

### f(x)=ax+b
ea=simplify('+'.join(['{0}*(a*{0}+b-{1})'.format(*d) for d in dots]))
eb=simplify('+'.join(['(a*{0}+b-{1})'.format(*d) for d in dots]))
#print(solve([ea,eb],[a,b])) #验证正确：a=310/43=7.209302325581396, b=-3170/43=-73.72093023255815

### f(x)=ax^2+bx+c
ea=simplify('+'.join(['{0}**2*(a*{0}**2+b*{0}+c-{1})'.format(*d) for d in dots]))
eb=simplify('+'.join(['{0}*(a*{0}**2+b*{0}+c-{1})'.format(*d) for d in dots]))
ec=simplify('+'.join(['(a*{0}**2+b*{0}+c-{1})'.format(*d) for d in dots]))

ret=solve([ea,eb,ec],[a,b,c])
f=lambda x: ret[a]*x**2+ret[b]*x+ret[c]
plt.plot(x,f(x),linestyle='-',color='pink',alpha=0.5,label='$f(x)={:.2}x^2{}{:.2}x{}{:.2}$'.format(ret[a].p/ret[a].q,'+' if ret[b]>0 else '',ret[b].p/ret[b].q,'+' if ret[c]>0 else '',ret[c].p/ret[c].q))

### f(x)=ax^3+bx^2+cx+d
ea=simplify('+'.join(['{0}**3*(a*{0}**3+b*{0}**2+c*{0}+d-{1})'.format(*d) for d in dots]))
eb=simplify('+'.join(['{0}**2*(a*{0}**3+b*{0}**2+c*{0}+d-{1})'.format(*d) for d in dots]))
ec=simplify('+'.join(['{0}*(a*{0}**3+b*{0}**2+c*{0}+d-{1})'.format(*d) for d in dots]))
ed=simplify('+'.join(['(a*{0}**3+b*{0}**2+c*{0}+d-{1})'.format(*d) for d in dots]))

ret=solve([ea,eb,ec,ed],[a,b,c,d])
f=lambda x: ret[a]*x**3+ret[b]*x**2+ret[c]*x+ret[d]
plt.plot(x,f(x),linestyle='-',color='green',alpha=0.7,label='$f(x)={:.2}x^3{}{:.2}x^2{}{:.2}x{}{:.2}$'.format(ret[a].p/ret[a].q,'+' if ret[b]>0 else '',ret[b].p/ret[b].q,'+' if ret[c]>0 else '',ret[c].p/ret[c].q,'+' if ret[d]>0 else '',ret[d].p/ret[d].q))

### f(x)=ax^4+bx^3+cx^2+dx+e
ea=simplify('+'.join(['{0}**4*(a*{0}**4+b*{0}**3+c*{0}**2+d*{0}+e-{1})'.format(*d) for d in dots]))
eb=simplify('+'.join(['{0}**3*(a*{0}**4+b*{0}**3+c*{0}**2+d*{0}+e-{1})'.format(*d) for d in dots]))
ec=simplify('+'.join(['{0}**2*(a*{0}**4+b*{0}**3+c*{0}**2+d*{0}+e-{1})'.format(*d) for d in dots]))
ed=simplify('+'.join(['{0}*(a*{0}**4+b*{0}**3+c*{0}**2+d*{0}+e-{1})'.format(*d) for d in dots]))
ee=simplify('+'.join(['(a*{0}**4+b*{0}**3+c*{0}**2+d*{0}+e-{1})'.format(*d) for d in dots]))

ret=solve([ea,eb,ec,ed,ee],[a,b,c,d,e])
f=lambda x: ret[a]*x**4+ret[b]*x**3+ret[c]*x**2+ret[d]*x+ret[e]
plt.plot(x,f(x),linestyle='-',color='blue',alpha=0.9,label='$f(x)={:.2}x^4{}{:.2}x^3{}{:.2}x^2{}{:.2}x{}{:.2}$'.format(ret[a].p/ret[a].q,'+' if ret[b]>0 else '',ret[b].p/ret[b].q,'+' if ret[c]>0 else '',ret[c].p/ret[c].q,'+' if ret[d]>0 else '',ret[d].p/ret[d].q,'+' if ret[e]>0 else '',ret[e].p/ret[e].q))

plt.legend(shadow=True)
plt.show()
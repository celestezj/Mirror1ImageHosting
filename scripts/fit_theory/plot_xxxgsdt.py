import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import Normalize
import numpy as np

dots=[(25,110),(27,115),(31,155),(33,160),(35,180)]
X,Y=zip(*dots)

f=lambda x: 7.1*x-72

x=np.linspace(24,36,2)
y=f(x)

x0=np.array(X)
y0=f(x0)

err=Y-y0

plt.errorbar(X,Y,abs(y0-Y)-0.5,uplims=err>0,lolims=err<0,fmt='ro',ecolor='black',elinewidth=1,capsize=2,markersize=5) #需要注意的是此处的-0.5纯粹是为了画出的图像美观，理论上是不应该有-0.5的
plt.plot(x,y,linestyle='--',color='g',alpha=0.4)

for i in dots:
    plt.annotate(str(i),(i[0]+0.1,i[1]),size=8)
plt.annotate(r'$f(x)=a·x+b$',(30,170),size=13,color='g')

plt.show()
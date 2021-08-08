import numpy as np
from numpy import linalg
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False
import os.path

def fit_poly(x,y,k=2):
    '''参数x和y是二维数据点的两个分量部分，都是一维数值序列，k表示多项式最高次数，默认取值2，表示二项式拟合，
       函数返回多项式函数以及系数列表，另外这个返回的多项式函数可以同时计算多个数值，如果你以列表传入的话'''
    n=len(x)
    if n!=len(y):
        raise ValueError("x's length must be equal to y's length!")
    X=np.zeros((n,k+1))
    X[:,0]=1
    X[:,1]=np.array(x)
    for i in range(2,k+1):
        X[:,i]=np.power(x,i)
    Y=np.array(y)[:,None]
    A=(linalg.inv(X.T.dot(X))).dot(X.T).dot(Y).flatten() #多项式系数列表（一个一维数组）
    expr='y='+'+'.join(['*'.join(['('+str(A[i])+')']+['x' for j in range(i)]) for i in range(k+1)]) #多项式函数的字符串形式
    def poly(x):
        x=np.array(x)
        d={'x':x}
        exec(expr,globals(),d)
        return d.get('y')
    return poly,A
    
xy=np.load(os.path.join(os.path.dirname(__file__),'xy.npz'))
x=xy['x']
y=xy['y']
plt.scatter(x,y,s=8,color='m',marker='s')

f,_=fit_poly(x,y,3) #三次多项式拟合

index=np.argsort(x)
a=np.linspace(*x[index][[2,-2]],200)

plt.plot(a,f(a),'g',label='二次多项式拟合')

f,_=fit_poly(x,y,9) #九次多项式拟合
plt.plot(a,f(a),'r',label='九次多项式拟合')

plt.legend()
plt.show()
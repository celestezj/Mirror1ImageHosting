import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from numpy import linalg
import matplotlib.cm as cm
from matplotlib.colors import Normalize

dots=[[1.1111111111111112, 0.0, 0.1138888380006059], [6.666666666666667, 0.0, 3.244091170716616], [8.88888888888889, 0.0, 2.698809112944384], [1.1111111111111112, 1.1111111111111112, 1.108735092622093], [2.2222222222222223, 1.1111111111111112, 1.368112983431465], [5.555555555555555, 1.1111111111111112, 1.7613284488843937], [8.88888888888889, 1.1111111111111112, 3.438603352774009], [10.0, 1.1111111111111112, 3.456650758385244], [1.1111111111111112, 2.2222222222222223, 1.893292787916852], [4.444444444444445, 2.2222222222222223, 3.274125651451564], [6.666666666666667, 2.2222222222222223, 3.480403972564556], [7.777777777777779, 2.2222222222222223, 3.4106953719863995], [8.88888888888889, 2.2222222222222223, 4.344706168208402], [10.0, 2.2222222222222223, 4.707765898892428], [2.2222222222222223, 3.3333333333333335, 4.636932995218534], [4.444444444444445, 3.3333333333333335, 5.463155206709421], [5.555555555555555, 3.3333333333333335, 4.158269592032508], [6.666666666666667, 3.3333333333333335, 5.021149961732221], [8.88888888888889, 3.3333333333333335, 4.786996720469217], [1.1111111111111112, 4.444444444444445, 4.483910794866308], [3.3333333333333335, 4.444444444444445, 3.977225357050014], [5.555555555555555, 4.444444444444445, 5.789822778606718], [6.666666666666667, 4.444444444444445, 5.501674770228268], [8.88888888888889, 4.444444444444445, 5.872842738606279], [10.0, 4.444444444444445, 6.994326159723737], [1.1111111111111112, 5.555555555555555, 7.718825578563116], [5.555555555555555, 5.555555555555555, 7.438913878229239], [6.666666666666667, 5.555555555555555, 6.266636056546943], [7.777777777777779, 5.555555555555555, 6.370191935134754], [8.88888888888889, 5.555555555555555, 5.921473346477713], [0.0, 6.666666666666667, 7.245724709880847], [3.3333333333333335, 6.666666666666667, 6.390072816055097], [4.444444444444445, 6.666666666666667, 6.788973206256314], [6.666666666666667, 6.666666666666667, 8.646435337058028], [8.88888888888889, 6.666666666666667, 8.338482180156962], [0.0, 7.777777777777779, 8.263820863361838], [1.1111111111111112, 7.777777777777779, 8.357603650042888], [2.2222222222222223, 7.777777777777779, 8.006012012424863], [3.3333333333333335, 7.777777777777779, 7.595571036619704], [7.777777777777779, 7.777777777777779, 9.220265069704816], [8.88888888888889, 7.777777777777779, 9.270927676078955], [10.0, 7.777777777777779, 8.34524267371918], [0.0, 8.88888888888889, 7.681685786807474], [5.555555555555555, 8.88888888888889, 7.741962799963534], [8.88888888888889, 8.88888888888889, 9.579428445412999], [1.1111111111111112, 10.0, 9.276935456509342], [2.2222222222222223, 10.0, 9.238545459448332], [3.3333333333333335, 10.0, 10.799244369297977], [4.444444444444445, 10.0, 9.400137873742473]]

'''
数据点生成：
import numpy as np
from math import sqrt

def f(x,y): #超平面
    return 0.38*1+0.225*x+0.86*y

n=100 #生成的最大点数（且处于[0,sqrt(n)]（x轴）、[0,sqrt(n)]（y轴）的正方形区域内）
k=0.5 #保留的比率
t=int(sqrt(n))
n=t*t

sigma=2
e=np.random.randn(n)*sigma #上下浮动误差

x=np.linspace(0,t,t)
y=x
x,y=np.meshgrid(x,y)

a=np.vstack((x.reshape(-1),y.reshape(-1),f(x,y).reshape(-1)+e))[:,np.random.rand(n)>k]

print(a.T.tolist())
'''

n=len(dots)

x,y,z=np.split(np.array(dots),3,axis=1)

X,Y=np.split(np.array(dots).T,[2,])
X=np.vstack((np.ones(n).reshape(1,-1),X))

fig=plt.figure()
ax=fig.gca(projection='3d')
ax.scatter(x,y,z,c=cm.hsv(Normalize(0,1)(np.linspace(0,1,n))))

theta=np.matmul(np.matmul(linalg.inv(np.matmul(X,X.T)),X),Y.T) #最小二乘矩阵法求解参数向量theta

print('通过最小二乘法得到的theta参数值:',theta)

def f(x,y):
    return theta[0]+theta[1]*x+theta[2]*y
    
_x,_y=np.meshgrid(np.linspace(-1,9,n),np.linspace(-1,9,n))
_z=f(_x,_y)

ax.plot_surface(_x,_y,_z,alpha=0.4)
plt.show()


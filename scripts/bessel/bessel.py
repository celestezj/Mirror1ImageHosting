import matplotlib.pyplot as plt
from numpy import fabs,linspace
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False

def fob(p1,p2,t):
    '''
    First-order Bessel
    一阶贝塞尔曲线，0个控制点，只有起点p1和终点p2，取值t时，0<=t<=1，求此时的轨迹点
    '''
    return ((1-t)*p1[0]+t*p2[0],(1-t)*p1[1]+t*p2[1])

def track_point_gen(*points,accuracy=None):
    '''
    args:
        points: a sequence of tuple point, 贝塞尔曲线的起点、多个控制点以及终点
        accuracy: a scalar, 精细度，用于设置绘制的轨迹曲线上的点的个数，默认值100
    returns:
        a list of historical tracked points , other process points and t
        返回一个列表，列表第一项是Bessel的历史轨迹点和当前轨迹点集合，列表第二项是绘制
        当前轨迹点的过程点集合，列表第三项是当前的t值
    '''
    backup=points
    accuracy=100 if accuracy==None else int(fabs(accuracy))
    history=[points[0]] #历史全部轨迹点集合
    for t in linspace(0,1,accuracy):
        others=[] #用于绘制Bessel曲线的其它过程点集，即出图中非Bessel的其它点，称“过程点”
        points=backup
        while len(points)>1:
            temp=[]
            for i,e in enumerate(points[1:],1):
                cur_point=fob(points[i-1],e,t) #当前轨迹点
                temp.append(cur_point)
            points=temp
            others.append(points)
        history.append(cur_point)
        yield [history,others,t]

def plot_bessel(*points,**kwargs):
    '''
    绘制贝塞尔曲线
    args:
        points: 两个端点和其它控制点，传递给track_point_gen()函数
        kwargs: Line2D属性以及accuracy参数，且除accuracy参数以外全部传递给plot()函数
    '''
    accuracy=kwargs.get('accuracy')
    if accuracy!=None:
        del kwargs['accuracy']
    lock=False
    for i,j,t in track_point_gen(*points,accuracy=accuracy):
        plt.cla()
        plt.title('Bessel曲线')
        plt.plot(*(zip(*points)),marker='o',linestyle='--',color='gray',alpha=0.5) #两个端点和几个控制点构成的大致轮廓
        for k in points:
            plt.annotate('({0:.1f},{1:.1f})'.format(k[0],k[1]),k,alpha=0.5) #点坐标
        for k in j:
            lines=plt.plot(*zip(*k),marker='o',alpha=0.3,markersize=3.5) #Bessel当前轨迹点的绘制过程
        bessel_line,*_=plt.plot(*zip(*i),**kwargs) #Bessel曲线
        plt.annotate('({0:.1f},{1:.1f})'.format(*j[-1][-1]),j[-1][-1]) #当前轨迹点坐标
        plt.plot(*zip(points[0],j[-1][-1]),marker='o',color=bessel_line.get_color(),linestyle='') #为贝塞尔曲线绘制两个端点
        if not lock:
            lock=True
            xlim,ylim=plt.gca().get_xlim(),plt.gca().get_ylim()
        plt.annotate('t={0:.2f}'.format(t),(xlim[1]-0.5,ylim[1]-0.2),bbox=dict(boxstyle="square",fc='pink'))
        plt.pause(0.1)
    plt.show()

if __name__=='__main__':
    #plot_bessel((1,1),(4,3)) #一阶示例
    plot_bessel((1,1),(2,3),(3.2,1.1),accuracy=30,color='r') #二阶
    #plot_bessel((1,1),(0.7,4),(3.4,4.1),(5,1),(7,2.7),(9,2.6),(6,8.5),accuracy=60,color='b') #六阶
    
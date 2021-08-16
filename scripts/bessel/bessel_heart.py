import numpy as np
import matplotlib.pyplot as plt

def fob(p1,p2,t):
    '''一阶贝塞尔'''
    return ((1-t)*p1[0]+t*p2[0],(1-t)*p1[1]+t*p2[1])

def track_point_gen(*points,accuracy=100):
    '''
    points: 贝塞尔曲线的起点、控制点和终点
    accuracy: 精细度，用于设置绘制的轨迹曲线上的点的个数，默认值100
    函数返回某一t（t取值0-1）时刻的曲线上的轨迹点以及上一个轨迹点，用于绘制连线
    '''
    backup=points
    accuracy=100 if accuracy==None else int(np.fabs(accuracy))
    last=points[0] #上一个轨迹点
    for t in np.linspace(0,1,accuracy):
        points=backup
        while len(points)>1:
            temp=[]
            for i,e in enumerate(points[1:],1):
                cur_point=fob(points[i-1],e,t) #当前轨迹点
                temp.append(cur_point)
            points=temp
        yield [last,points[0]]
        last=cur_point

def plot_bessel(*points,**kwargs):
    '''
    绘制贝塞尔曲线（主函数）
    points: 两个端点和控制点
    kwargs: Line2D属性以及accuracy（精确度）、animation（是否动画绘制，默认是）、all_points
        （全部点，用于预定义画布大小和初始化画布底板）参数，且除accuracy、animation、
        all_points参数以外全部传递给plot()函数
    注，all_points参数：假设我们要在一个画布上先后绘制两个贝塞尔曲线，两次使用的点集不一样，
        但是我们希望画布底板预先给出全部点，就可以通过该参数进行设置，具体自行实验
    '''
    accuracy=kwargs.get('accuracy')
    if accuracy!=None:
        del kwargs['accuracy']
    animation=kwargs.get('animation')
    if animation!=None:
        del kwargs['animation']
    else:
        animation=True
    all_points=kwargs.get('all_points')
    if all_points!=None:
        del kwargs['all_points']
    else:
        all_points=points
    plt.plot(*(zip(*all_points)),marker='o',linestyle='--',color='gray',alpha=0.2) #置为white
    gen=track_point_gen(*points,accuracy=accuracy)
    if animation:
        for i in gen:
            plt.plot(*zip(i[0],i[1]),**kwargs)
            plt.pause(0.05)
    else:
        a=np.array([i[1] for i in gen])
        plt.plot(a[:,0],a[:,1],**kwargs)

if __name__=='__main__':
    plt.ion()
    #plot_bessel((0,0),(-0.5,3),(4,3.2),(5,0.1),(6.2,2.5),accuracy=50,color='r',animation=False) #test
    #一颗爱心
    left_points=[(0,0),(-0.5,1.6),(-1.2,1.2),(-1.6,0),(-1.8,-2),(-1.5,-3.2),(-0.7,-4.6),(0,-6)] # 左半平面点集
    #left_points=[(0,0),(-1.3,1),(-4,0.5),(-4.5,-2),(0,-3)]
    right_points=[(-i[0],i[1]) for i in left_points][::-1] # 右半平面点集
    plot_bessel(*left_points,color='r',all_points=left_points+right_points,accuracy=40)
    plot_bessel(*right_points[::-1],color='b',accuracy=40)
    plt.ioff()
    plt.show()
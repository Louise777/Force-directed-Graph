import json
import random
import math
import matplotlib.pyplot as plt

CANVAS_WIDTH = 2000
CANVAS_HEIGHT = 2000

#计算两个Node的斥力产生的单位位移
def calculateRepulsive(Nodes,k):
    ejectFactor = 6
    for i in Nodes:
        nodei=Nodes[i]
        nodei['Dx']=0.0
        nodei['Dy']=0.0
        for j in Nodes:
            if(i!=j):
                nodej=Nodes[j]
                distX=nodei['x']-nodej['x']
                distY=nodei['y']-nodej['y']
                dist=math.sqrt(distX*distX+distY*distY)
                if(dist<30):
                    ejectFactor=5
                if(dist>0 and dist<250):
                    nodei['Dx']=nodei['Dx']+distX/dist*k*k/dist*ejectFactor
                    nodei['Dy']=nodei['Dy']+distY/dist*k*k/dist*ejectFactor

#计算Edge对两端Node产生的引力
def calculateTraction(Nodes,Edges,k):
    condenseFactor = 3;
    for e in Edges:
        startId=e['source']
        endId=e['target']
        distX=Nodes[startId]['x']-Nodes[endId]['x']
        distY=Nodes[startId]['y']-Nodes[endId]['y']
        dist=math.sqrt(distX*distX+distY*distY)
        Nodes[startId]['Dx']=Nodes[startId]['Dx']- distX * dist / k * condenseFactor
        Nodes[startId]['Dy']=Nodes[startId]['Dy']- distY * dist / k * condenseFactor
        Nodes[endId]['Dx']=Nodes[endId]['Dx']+ distX * dist / k * condenseFactor
        Nodes[endId]['Dy']=Nodes[endId]['Dy']+ distY * dist / k * condenseFactor
     
#更新坐标   
def updateCoordinates(Nodes):
    maxt = 4 
    maxty = 3  #Additional coefficients.
    for e in Nodes:
        node=Nodes[e]
        dx=math.floor(node['Dx'])
        dy=math.floor(node['Dy'])
        
        if(dx<-maxt):
            dx=-maxt
        if(dx>maxt):
            dx=maxt
        if(dy<-maxty):
            dy=-maxty
        if(dy>maxty):
            dy=maxty
        if(node['x']+dx>=CANVAS_WIDTH or node['x']+dx<=0):
            node['x']=node['x']-dx
        else:
            node['x']=node['x']+dx
        if(node['y']+dy>=CANVAS_HEIGHT or node['y']+dy<=0):
            node['y']=node['y']-dy
        else:
            node['y']=node['y']+dy
        
        

#读取json数据
with open("data.json",'r') as load_f:
    chart = json.load(load_f)

#随机生成初始坐标
Nodes=dict()
for e in chart['nodes']:
    rand_x=random.randint(0,CANVAS_WIDTH)
    rand_y=random.randint(0,CANVAS_HEIGHT)
    Nodes[e['id']]=dict({'x':rand_x,'y':rand_y,'group':e['group'],'Dx':0.0,'Dy':0.0})
    
k=math.sqrt(CANVAS_WIDTH * CANVAS_HEIGHT / len(Nodes))

#迭代200次
for i in range(200):
    calculateRepulsive(Nodes,k);
    calculateTraction(Nodes,chart['links'],k);
    updateCoordinates(Nodes);

#绘图
for e in Nodes:
    plt.scatter(Nodes[e]['x'],Nodes[e]['y'],s=10,c='k')
for edge in chart['links']:
    startId=edge['source']
    endId=edge['target']
    plt.plot([Nodes[startId]['x'],Nodes[endId]['x']],[Nodes[startId]['y'],Nodes[endId]['y']],linewidth=0.5,c='k')
plt.show()
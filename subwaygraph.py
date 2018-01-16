# -*- coding: utf-8 -*-

import dict.py

INF = float('inf')

class Vertex:
    def __init__(self, key):
        self.id = key
        self.connectedTo = {}

    def addNeighbor(self, nbr, weight=0):
        self.connectedTo[nbr] = weight

    def __str__(self):
        return str(self.id) + ' connectedTo: ' + str([x.id for x in self.connectedTo])

    def getConnections(self):
        return self.connectedTo.keys()

    def getId(self):
        return self.id

    def getWeight(self, nbr):
        if nbr in self.getConnections():
            return self.connectedTo[nbr]
        elif nbr.getId() == self.getId():
            return 0
        else:
            return INF


class Graph:
    def __init__(self):
        self.vertList = {}
        self.numVertices = 0
        self.path = ''

    def addVertex(self, key):
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key)
        self.vertList[key] = newVertex
        return newVertex

    def getVertex(self, n):
        if n in self.vertList:
            return self.vertList[n]
        else:
            return None

    def __contains__(self, n):
        return n in self.vertList

    def addEdge(self, f, t, cost=0):
        if f not in self.vertList:
            nv = self.addVertex(f)
        if t not in self.vertList:
            nv = self.addVertex(t)
        self.vertList[f].addNeighbor(self.vertList[t], cost)

    def getVertices(self):
        return self.vertList.keys()

    def __iter__(self):
        return iter(self.vertList.values())

    def findPath(self, src, dst, dis, fromdst):
        '''
        从路程表逆推求路径
        '''
        if dst == src:
            return
        if fromdst == 1:   #路程表的方向是从dst到src
            for v in dis.keys():
                if self.vertList[v] in self.vertList[dst].getConnections() and dis[v] < dis[dst]:
                    self.path = v + ' - ' +self.path
                    self.findPath(src, v, dis, fromdst) #将v添加到路径，并继续寻找从src到v的路径
                    return
        else:               #路程表的方向是从src到dst
            for v in dis.keys():
                if self.vertList[v] in self.vertList[src].getConnections() and dis[v] < dis[src]:
                    self.path = self.path + ' - ' +v
                    self.findPath(v, dst, dis, fromdst) #将v添加到路径，并继续寻找从v到dst的路径
                    return

    def dijkstra(self, src, dst):
        '''
        双向dijkstra算法寻找最短路径

        同名变量中，后缀为1的从出发点开始计算，后缀为2的从终点开始
        book:已经过的点
        cur:当前的点
        dis:从计算起点开始经过的路程时间
        '''
        book1 = set()
        book2 = set()
        cur1 = self.vertList[src]
        dis1 = dict((k,INF) for k in self.vertList)
        dis1[src] = 0
        cur2 = self.vertList[dst]
        dis2 = dict((k,INF) for k in self.vertList)
        dis2[dst] = 0
        while len(book1) + len(book2) < len(self.getVertices()):    #遍历所有点
            book1.add(cur1)
            book2.add(cur2)
            for v in cur1.getConnections():                         #从出发点更新路程表
                if dis1[cur1.getId()] + v.getWeight(cur1) < dis1[v.getId()]:    #路程满足三角关系，则更新路程表
                    dis1[v.getId()] = dis1[cur1.getId()] + v.getWeight(cur1)
            for v in cur2.getConnections():                         #从终点更新路程表
                if dis2[cur2.getId()] + v.getWeight(cur2) < dis2[v.getId()]:
                    dis2[v.getId()] = dis2[cur2.getId()] + v.getWeight(cur2)
            if cur2.getId() in book1:                               #若两个路径经过了同一个点A，下同
                self.path = cur2.getId()
                self.findPath(src, cur2.getId(), dis1, 1)           #寻找出发点-点A的路径
                self.findPath(cur2.getId(), dst, dis2, 0)           #寻找点A-终点的路径
                print('路线为：',self.path)
                return dis1[cur2.getId()]+dis2[cur2.getId()]
            elif cur1 in book2:
                self.path = cur1.getId()
                self.findPath(src, cur1.getId(), dis1, 1)
                self.findPath(cur1.getId(), dst, dis2, 0)
                print('路线为：',self.path)
                return dis1[cur1.getId()]+dis2[cur1.getId()]
            new1 = INF
            new2 = INF
            for v in dis1.keys():                                   #下一个计算点
                if self.vertList[v] in book1:
                    continue
                if dis1[v] < new1:
                    new1 = dis1[v]
                    cur1 = self.vertList[v]
            for v in dis2.keys():
                if self.vertList[v] in book2:
                    continue
                if dis2[v] < new2:
                    new2 = dis2[v]
                    cur2 = self.vertList[v]
        return dis[dst]

if __name__ == "__main__":

    g = Graph()

    vel = 10  # 地铁的速度 m/s

    for x in subway_dict:
        g.addEdge(x[0], x[1], (float)(x[2]) / vel)  # 由距离得到时间
        g.addEdge(x[1], x[0], (float)(x[2]) / vel)  # 双向都有

    for x in transfer_dict:
        g.addEdge(x[0], x[1], (float)(x[2]))  # 换站给的直接就是时间

    #print('最短时间为：%.2fs' % (g.dijkstra('1-天安门西', '13-西二旗')))
    #print('最短时间为：%.2fs' % (g.dijkstra("CP-沙河", 'YZ-宋家庄')))
    print('最短时间为：%.2fs' % (g.dijkstra("14E-来广营", '14W-园博园')))

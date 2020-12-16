#! /usr/bin/env python

from time import time

tiempo_inicial = time()

FILE_NAME = "C:\\Users\\JuanCarlos\\Desktop\\master-ipr\\map12\\map12.csv"
START_X = 2
START_Y = 2
END_X = 2
END_Y = 15
class Node:
    def __init__(self, x, y, myId, parentId):
        self.x = x
        self.y = y
        self.myId = myId
        self.parentId = parentId
    def dump(self):
        print("---------- x "+str(self.x)+\
                         " | y "+str(self.y)+\
                         " | id "+str(self.myId)+\
                         " | parentId "+str(self.parentId))

nodes = []

init = Node(START_X, START_Y, 0, -2)
# init.dump()

nodes.append(init)

charMap = []

def dumpMap():
    for line in charMap:
        print(line)

with open(FILE_NAME) as f:
    line = f.readline()
    while line:
        charLine = line.strip().split(',')
        charMap.append(charLine)
        line = f.readline()

charMap[START_X][START_Y] = '3'
charMap[END_X][END_Y] = '4'

dumpMap()

done = False
goalParentId = -1
iteraciones = 0
while not done:
    for node in nodes:
        print("--------------------- number of nodes: "+str(len(nodes)))
        node.dump()
        # up
        iteraciones = iteraciones + 1
        print("El numero de iteraciones es: " + str(iteraciones))
        tmpX = node.x - 1
        tmpY = node.y
        if( charMap[tmpX][tmpY] == '4' ):
            print("up: GOALLLL!!!")
            goalParentId = node.myId
            done = True
            break
        elif ( charMap[tmpX][tmpY] == '0' ):
            print("up: mark visited")
            newNode = Node(tmpX, tmpY, len(nodes), node.myId)
            charMap[tmpX][tmpY] = '2'
            nodes.append(newNode)

        # down
        tmpX = node.x + 1
        tmpY = node.y
        if( charMap[tmpX][tmpY] == '4' ):
            print("down: GOALLLL!!!")
            goalParentId = node.myId
            done = True
            break
        elif ( charMap[tmpX][tmpY] == '0' ):
            print("down: mark visited")
            newNode = Node(tmpX, tmpY, len(nodes), node.myId)
            charMap[tmpX][tmpY] = '2'
            nodes.append(newNode)

        # right
        tmpX = node.x
        tmpY = node.y + 1
        if( charMap[tmpX][tmpY] == '4' ):
            print("right: GOALLLL!!!")
            goalParentId = node.myId
            done = True
            break
        elif ( charMap[tmpX][tmpY] == '0' ):
            print("right    : mark visited")
            newNode = Node(tmpX, tmpY, len(nodes), node.myId)
            charMap[tmpX][tmpY] = '2'
            nodes.append(newNode)

        # left
        tmpX = node.x
        tmpY = node.y - 1
        if( charMap[tmpX][tmpY] == '4' ):
            print("left: GOALLLL!!!")
            goalParentId = node.myId
            done = True
            break
        elif ( charMap[tmpX][tmpY] == '0' ):
            print("left: mark visited")
            newNode = Node(tmpX, tmpY, len(nodes), node.myId)
            charMap[tmpX][tmpY] = '2'
            nodes.append(newNode)

        dumpMap()

print("%%%%%%%%%%%%%%%%%%%")
ok = False
nodos_camino = 0
while not ok:
    for node in nodes:
        if( node.myId == goalParentId ):
            nodos_camino = nodos_camino + 1
            node.dump()
            goalParentId = node.parentId
            if( goalParentId == -2):
                print("El numero de nodos del camino es: " + str(nodos_camino))
                tiempo_final = time()
                tiempo_ejecucion = tiempo_final - tiempo_inicial
                print("EL tiempo de ejecucion ha sido: " + str(tiempo_ejecucion))
                print("%%%%%%%%%%%%%%%%%2")
                ok = True

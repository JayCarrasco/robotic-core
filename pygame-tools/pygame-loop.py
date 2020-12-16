#!/usr/bin/env python

import pygame
import time
import sys

# Parse CLI arguments
if (len(sys.argv) != 4):
    print("./pygame-loop.py map1.csv 2 2")
    quit()
inFileStr = sys.argv[1]
initX = int(sys.argv[2])
initY = int(sys.argv[3])

# Extracting nX(rows) and nY(columns) from file
from numpy import genfromtxt
inFile = genfromtxt(inFileStr, delimiter=',')
nX = inFile.shape[0]
nY = inFile.shape[1]

END_X = 4
END_Y = 9

inFile[END_X][END_Y] = 4

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
COLOR_BACKGROUND = (0, 0, 0)
COLOR_WALL = (255, 255, 255)
COLOR_ROBOT = (255, 0, 0)
COLOR_GOAL = (255, 0, 255)

SIM_PERIOD_MS = 500.0

#hight and width of each pixel
pixelX = SCREEN_WIDTH/nX
pixelY = SCREEN_HEIGHT/nY

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
screen.fill(COLOR_BACKGROUND)

#node class--adapting to the current problem
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


# Node list
nodes = []

#Node list initialization
init = Node(initX, initY, 0, -2)

nodes.append(init)

class SimRender:
    def __init__(self, robotX, robotY):
        for iX in range(nX):
            #print "iX:",iX
            for iY in range(nY):
                #print "* iY:",iY

                #-- Skip box if map indicates a 0
                if inFile[iX][iY] == 0:
                    continue

                pygame.draw.rect(screen, COLOR_WALL,
                                 pygame.Rect( pixelX*iX, pixelY*iY, pixelX, pixelY ))

                if inFile[iX][iY] == 4:
                	pygame.draw.rect(screen, COLOR_GOAL, 
                					 pygame.Rect( pixelX*iX, pixelY*iY, pixelX, pixelY ))

                self.robot = pygame.draw.rect(screen, COLOR_ROBOT,
                                              pygame.Rect( pixelX*initX+pixelX/4.0, pixelY*initY+pixelY/4.0, pixelX/2.0, pixelY/2.0 ))
        pygame.display.flip()

    def moveRobot(self, incrementX, incrementY):
        pygame.draw.rect(screen, COLOR_BACKGROUND, self.robot)
        self.robot.move_ip(incrementX, incrementY)
        pygame.draw.rect(screen, COLOR_ROBOT, self.robot)
        pygame.display.update()

simRender = SimRender(initX, initY)
time.sleep(0.5)

done = False
while not done:
    for node in nodes:
        print("--------------------- number of nodes: "+str(len(nodes)))
        node.dump()

        #tmpX and tmpY are the positions on the map of the current node
        #up
        tmpX = node.x - 1
        tmpY = node.y
        if( inFile[tmpX][tmpY] == 4):
            print("up: GOALLLL!!!")
            goalParentId = node.myId
            done = True
            break

        elif ( inFile[tmpX][tmpY] == 0 ):
            print("up: mark visited")
            newNode = Node(tmpX, tmpY, len(nodes), node.myId)
            inFile[tmpX][tmpY] = 2
            nodes.append(newNode)

        # down
        tmpX = node.x + 1
        tmpY = node.y
        if( inFile[tmpX][tmpY] == 4 ):
            print("down: GOALLLL!!!")
            goalParentId = node.myId
            done = True
            break
        elif ( inFile[tmpX][tmpY] == 0 ):
            print("down: mark visited")
            newNode = Node(tmpX, tmpY, len(nodes), node.myId)
            inFile[tmpX][tmpY] = 2
            nodes.append(newNode)

        # right
        tmpX = node.x
        tmpY = node.y + 1
        if( inFile[tmpX][tmpY] == 4 ):
            print("right: GOALLLL!!!")
            goalParentId = node.myId
            done = True
            break
        elif ( inFile[tmpX][tmpY] == 0 ):
            print("right    : mark visited")
            newNode = Node(tmpX, tmpY, len(nodes), node.myId)
            inFile[tmpX][tmpY] = 2
            nodes.append(newNode)

        # left
        tmpX = node.x
        tmpY = node.y - 1
        if( inFile[tmpX][tmpY] == 4 ):
            print("left: GOALLLL!!!")
            goalParentId = node.myId
            done = True
            break
        elif ( inFile[tmpX][tmpY] == 0 ):
            print("left: mark visited")
            newNode = Node(tmpX, tmpY, len(nodes), node.myId)
            inFile[tmpX][tmpY] = 2
            nodes.append(newNode)

final = Node(END_X, END_Y, goalParentId+1, goalParentId+2) 

print("%%%%%%%%%%%%%%%%%%%")
ok = False
nodos_camino = 0
nodos_final = []
while not ok:
    for node in nodes:
        if( node.myId == goalParentId ):
            nodos_camino = nodos_camino + 1
            nodos_final.append(node)
            node.dump()
            goalParentId = node.parentId
            if( goalParentId == -2):
                print("El numero de nodos del camino es: " + str(nodos_camino))
                print("%%%%%%%%%%%%%%%%%2")
                ok = True

nodos_final.append(final)


nodos_final.sort(key = lambda x:x.myId, reverse = False)

x1 = initX;
y1 = initY;

for node in nodos_final:
	x2 = node.x
	y2 = node.y
	resta_x = x2 - x1
	resta_y = y2 - y1
	simRender.moveRobot(resta_x*pixelX,resta_y*pixelY)
	time.sleep(SIM_PERIOD_MS/1000.0)
	done = False
	x1 = node.x
	y1 = node.y

	print("myId", node.myId)
	print("x", node.x)
	print("y", node.y)
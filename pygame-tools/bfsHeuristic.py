#! /usr/bin/env python
"Import libraries"
import pygame
import time
import sys
import random

"Declaracion de la ruta del archivo csv, que es el mapa en el que vamos a realizar la busqueda"
FILE_NAME = "map1.csv"

"Se pasa como argumento al programa el mapa y las coordenadas de comienzo"
# Parse CLI arguments
if (len(sys.argv) != 4):
    print("./bfsHeuristic.py map1.csv 2 2")
    quit()
inFileStr = sys.argv[1]
initX = int(sys.argv[2])
initY = int(sys.argv[3])

"Declaracion de las coordenadas de la meta"
END_X = 7
END_Y = 2

from numpy import genfromtxt
inFile = genfromtxt(inFileStr, delimiter=',')
nX = inFile.shape[0]
nY = inFile.shape[1]

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
COLOR_BACKGROUND = (0, 0, 0)
COLOR_WALL = (255, 255, 255)
COLOR_ROBOT = (255, 0, 0)

SIM_PERIOD_MS = 500.0

pixelX = SCREEN_WIDTH/nX
pixelY = SCREEN_HEIGHT/nY

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
screen.fill(COLOR_BACKGROUND)

"Clase nodo para crear instancias de nodos. Coordenadas x e y en el plano, ademas de su ID y el de su nodo padre"
"Como tiene en cuenta costes, metemos costetotal y costemeta"
class Node:
    def __init__(self, x, y, myId, parentId, weight):
        self.x = x
        self.y = y
        self.myId = myId
        self.parentId = parentId
        self.weight = weight
    def dump(self):
        print("---------- x "+str(self.x)+\
                         " | y "+str(self.y)+\
                         " | id "+str(self.myId)+\
                         " | parentId "+str(self.parentId)+\
                         " | weight " +str(self.weight))

class SimRender:
    def __init__(self, robotX, robotY):
        for iX in range(nX):
            #print "iX:",iX
            for iY in range(nY):
                #print "* iY:",iY

                #-- Skip box if map indicates a 0
                if inFile[iX][iY] == 0:
                    continue

                pygame.draw.rect(screen, COLOR_WALL, pygame.Rect( pixelX*iX, pixelY*iY, pixelX, pixelY ))
                self.robot = pygame.draw.rect(screen, COLOR_ROBOT, pygame.Rect( pixelX*initX+pixelX/4.0, pixelY*initY+pixelY/4.0, pixelX/2.0, pixelY/2.0 ))

        pygame.display.flip()

    def moveRobot(self, incrementX, incrementY):
        pygame.draw.rect(screen, COLOR_BACKGROUND, self.robot)
        self.robot.move_ip(incrementX, incrementY)
        pygame.draw.rect(screen, COLOR_ROBOT, self.robot)
        pygame.display.update()

simRender = SimRender(initX, initY)
time.sleep(0.5)


"Funcion para calcular el coste utilizando la distancia Manhattan"
def calculoCoste(x, y, startx, starty, endx, endy):
    "Calculo la distancia entre el nodo y el origen"
    coste_O = abs(x- startx) + abs(y - starty)
    "Calculo la distancia entre el nodo y la meta"
    coste_M = abs(x - endx) + abs(y - endy)
    "Calculo el coste total"
    coste_T = coste_O + coste_M
    return coste_T, coste_M, coste_O
    
"Declaracion de la lista de nodos"
nodes = []

"Declaracion de la lista de costes [coste_T, coste_M, coste_O]"
weight = []

"Inicializacion del primer nodo"
weight = calculoCoste(initX, initY, initX, initY , END_X, END_Y)
init = Node(initX, initY, 0, -2, weight[0])
# init.dump()

"Inserta el primer nodo en la lista de nodos"
nodes.append(init)

"Declaracion de la lista de caracteres del mapa"
charMap = []

with open(FILE_NAME) as f:
    line = f.readline()
    while line:
        charLine = line.strip().split(',')
        charMap.append(charLine)
        line = f.readline()

"Asignacion del caracter 3 al punto inicial y caracter 4 al punto final"
charMap[initX][initY] = '3'
charMap[END_X][END_Y] = '4'

"Declaracion de variables que usamos en el algoritmo de busqueda"
done = False               
goalParentId = -1      
iteraciones = 0         
n_vecinos_x = []
n_vecinos_y = []
vecinosOcupados = 0

"Bucle infinito. Mientras no encuentre la meta continua iterando"
while not done:
    print("--------------------- number of nodes: "+str(len(nodes)))
    "Al ser un algoritmo de busqueda greedy, el ultimo nodo que se encuentra es el siguiente en usarse"
    "Por lo tanto, bucle for hacia atras"
    for node_v in range(len(nodes)-1, -1, -1):
        print("El nodo es el numero: " + str(node_v))
        "Se llama al nodo actual"
        nodes[node_v].dump()
        "n_vecinos_x y n_vecinos_y para guardar los valores de los vecinos"                   
        n_vecinos_x = [nodes[node_v].x, nodes[node_v].x+1, nodes[node_v].x-1]
        n_vecinos_y = [nodes[node_v].y, nodes[node_v].y+1, nodes[node_v].y-1]
        
        "Hago aleatoria la eleccion de x e y para que no se haga determinista"
        random.shuffle(n_vecinos_x)
        random.shuffle(n_vecinos_y)
        
        "Inicializamos vecinosOcupados, que es la variable que determina cuantos vecinos no estan libres"
        "en el nodo actual"
        vecinosOcupados = 0
        menorcostetotal = 1000
        menorcostemeta = 1000
        "Recorremos los vecinos, y se escoge el que tenga menor costetotal y coste de meta"
        for vecinosX in n_vecinos_x:
            for vecinosY in n_vecinos_y:
                if ((charMap[vecinosX][vecinosY] == '2') or (charMap[vecinosX][vecinosY] == '1') 
                or (charMap[vecinosX][vecinosY] == '3')):
                    vecinosOcupados = vecinosOcupados + 1
                elif((charMap[vecinosX][vecinosY] == '0') or (charMap[vecinosX][vecinosY] == '4')):
                    weight = calculoCoste(vecinosX, vecinosY, initX, initY, END_X, END_Y)
                    print("coste: "+str(weight));
                    if (weight[0] <= menorcostetotal):
                        menorcostetotal = weight[0]
                        print("menorcostetotal: "+str(menorcostetotal));
                        if (weight[1] < menorcostemeta):
                            menorcostemeta = weight[1]
                            tmpX = vecinosX
                            tmpY = vecinosY
                            print("menorcostemeta: "+str(menorcostemeta));
                                        
                
        print("El numero de vecinosOcupados es: " + str(vecinosOcupados))                                
        iteraciones = iteraciones + 1
        print("El numero de iteraciones es: " + str(iteraciones))
    
        "Si encuentro la meta, done=true para acabar con el bucle"
        "Si encuentro un sitio libre, que no es la meta, incluyo este nuevo nodo a la lista de nodos"
        "y le pongo como visitado en el charMap"
        if( charMap[tmpX][tmpY] == '4' ):
            print("up: GOALLLL!!!")
            goalParentId = nodes[node_v].myId
            done = True
            break
        elif ( charMap[tmpX][tmpY] == '0' ):
            print("mark visited")
            newNode = Node(tmpX, tmpY, len(nodes), nodes[node_v].myId, menorcostetotal)
            charMap[tmpX][tmpY] = '2'
            nodes.append(newNode)
            break

print("%%%%%%%%%%%%%%%%%%%")
ok = False
nodos_camino = 0
while not ok:
    for node in nodes:
        if( node.myId == goalParentId ):
            simRender.moveRobot(node.x, node.y)
            time.sleep(SIM_PERIOD_MS/1000.0)
            node.dump()
            goalParentId = node.parentId











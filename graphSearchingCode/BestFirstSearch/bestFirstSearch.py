#! /usr/bin/env python
"Importación de la librería random para dar aleatoriedad a la búsqueda más adelante"
import random

"Importación de la librería time para contar el tiempo de ejecucion"
from time import time

"Inicio de la ejecución"
tiempo_inicial = time()

"Declaración de la ruta del archivo csv, que es el mapa en el que vamos a realizar la búsqueda"
FILE_NAME = "C:\\Users\\JuanCarlos\\Desktop\\master-ipr\\map1\\map1.csv"

"Declaración del punto inicial y meta"
START_X = 2
START_Y = 2
END_X = 7
END_Y = 2

"Clase nodo para crear instancias de nodos. Coordenadas x e y en el plano, además de su ID y el de su nodo padre"
"Como tiene en cuenta costes, metemos costetotal y costemeta"
class Node:
    def __init__(self, x, y, myId, parentId, costetotal, costemeta):
        self.x = x
        self.y = y
        self.myId = myId
        self.parentId = parentId
        self.costetotal = costetotal
        self.costemeta = costemeta
    def dump(self):
        print("---------- x "+str(self.x)+\
                         " | y "+str(self.y)+\
                         " | id "+str(self.myId)+\
                         " | parentId "+str(self.parentId)+\
                         " | costetotal " +str(self.costetotal)+\
                         " | costemeta " + str(self.costemeta))
                         

"Función dumpMap, que dibuja el mapa"
def dumpMap():
    for line in charMap:
        print(line)

"Función para calcular el coste utilizando la distancia Manhattan"
def calculoCoste(x, y, startx, starty, endx, endy):
    "Calculo la distancia entre el nodo y el origen"
    coste_O = abs(x- startx) + abs(y - starty)
    "Calculo la distancia entre el nodo y la meta"
    coste_M = abs(x - endx) + abs(y - endy)
    "Calculo el coste total"
    coste_T = coste_O + coste_M
    return coste_T, coste_M, coste_O
    
"Declaración de la lista de nodos"
nodes = []

"Declaración de la lista de costes [coste_T, coste_M, coste_O]"
weight = []

"Inicialización del primer nodo"
weight = calculoCoste(START_X, START_Y, START_X, START_Y, END_X, END_Y)
init = Node(START_X, START_Y, 0, -2, weight[0], weight[1])
# init.dump()

"Inserta el primer nodo en la lista de nodos"
nodes.append(init)

"Declaración de la lista de caracteres del mapa"
charMap = []

"¿COMO SABE QUE TIENE QUE LEER TODAS LAS LINEAS Y NO SOLO LA PRIMERA? -- PREGUNTAR"
with open(FILE_NAME) as f:
    line = f.readline()
    while line:
        charLine = line.strip().split(',')
        charMap.append(charLine)
        line = f.readline()

"Asignación del caracter 3 al punto inicial y caracter 4 al punto final"
charMap[START_X][START_Y] = '3'
charMap[END_X][END_Y] = '4'

"Llamada a función dumpMap para dibujar el mapa"
dumpMap()

"Declaración de variables que usamos en el algoritmo de búsqueda"
done = False               
goalParentId = -1      
iteraciones = 0         
n_vecinos_x = []
n_vecinos_y = []
vecinosOcupados = 0

"Bucle infinito. Mientras no encuentre la meta continúa iterando"
while not done:
    print("--------------------- number of nodes: "+str(len(nodes)))
    "Al ser un algoritmo de búsqueda greedy, el último nodo que se encuentra es el siguiente en usarse"
    "Por lo tanto, bucle for hacia atrás"
    for node_v in range(len(nodes)-1, -1, -1):
        "Inicializamos la variable encontrado"
        encontrado = False  
        "Se dibuja el mapa"
        dumpMap()
        print("El nodo es el numero: " + str(node_v))
        "Se llama al nodo actual"
        nodes[node_v].dump()
        "n_vecinos_x y n_vecinos_y para guardar los valores de los vecinos"                   
        n_vecinos_x = [nodes[node_v].x, nodes[node_v].x+1, nodes[node_v].x-1]
        n_vecinos_y = [nodes[node_v].y, nodes[node_v].y+1, nodes[node_v].y-1]
        
        "Hago aleatoria la elección de x e y para que no se haga determinista"
        random.shuffle(n_vecinos_x)
        random.shuffle(n_vecinos_y)
        
        "Inicializamos vecinosOcupados, que es la variable que determina cuántos vecinos no están libres"
        "en el nodo actual"
        vecinosOcupados = 0
        encontrado = False
        "Recorremos los vecinos en búsqueda de uno que esté libre o que sea la meta"
        "Cuando lo encuentra deja de ejecutar el bucle"
        for vecinosX in n_vecinos_x:
            for vecinosY in n_vecinos_y:
                if ((charMap[vecinosX][vecinosY] == '2') or (charMap[vecinosX][vecinosY] == '1') 
                or (charMap[vecinosX][vecinosY] == '3')):
                    vecinosOcupados = vecinosOcupados + 1
                elif((charMap[vecinosX][vecinosY] == '0') or (charMap[vecinosX][vecinosY] == '4')):
                    "se calculan los costes del nodo"
                    weight = calculoCoste(vecinosX, vecinosY, START_X, START_Y, END_X, END_Y)
                    costetotal = weight[0]
                    costemeta = weight[1]
                    tmpX = vecinosX
                    tmpY = vecinosY
                    "Si encuentra la meta, pongo done a true para finalizar"
                    if( charMap[tmpX][tmpY] == '4' ):
                        print("up: GOALLLL!!!")
                        goalParentId = nodes[node_v].myId
                        done = True
                        break
                    elif ( charMap[tmpX][tmpY] == '0' ):
                        print("mark visited")
                        newNode = Node(tmpX, tmpY, len(nodes), nodes[node_v].myId, costetotal, costemeta)
                        charMap[tmpX][tmpY] = '2'
                        nodes.append(newNode)
                        encontrado = True
                        break
                    print("coste: "+str(weight));
            "Si encuentra un nodo vacío, sale del bucle"
            if (encontrado == True) :
                break
        if (vecinosOcupados == 9):
            nodes[node_v].costemeta = 1000
        print("El numero de vecinosOcupados es: " + str(vecinosOcupados))                                
        iteraciones = iteraciones + 1
        print("El numero de iteraciones es: " + str(iteraciones))
        "Ordenamos la lista de nodos por coste"
        nodes.sort(key = lambda x:x.costemeta, reverse = True)
        if (encontrado == True):
            break


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
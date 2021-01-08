#SE IMPORTA ROSPY, LOS MENSAJES Y LAS LIBRERIAS QUE SE VAN A USAR
import rospy
from trabajo.msg import usuario,testAction,testGoal
from std_msgs.msg import Bool,String
from trabajo.srv import duplica
import os
import actionlib
#FUNCION QUE DEFINE EL CLIENTE DEL ACTIONLIB
def action_lib_client(name):
	#SE DEFINE EL CLIENTE
	client = actionlib.SimpleActionClient('deletrea', testAction)

	#SE COMPRUEBA SI EL CLIENTE RESPONDE EN UN PLAZO CORTO (0.5S)
	if client.wait_for_server(rospy.Duration(0.5)):

		#DEFINIMOS EL GOAL, EN ESTE CASO EL NOMBRE A DELETREAR
		goal = testGoal(name)

		#LO ENVIA
		client.send_goal(goal)

		#SE ESPERA QUE ACABE DE DELETREAR PARA CONTINUAR LA EJECUCION
		client.wait_for_result()

	#SI NO TIENE RESPUESTA DEL SERVIDOR INDICA QUE ESTA APAGADO
	else:
		print("El actionlib no esta conectado")


#CLIENTE DEL SERVICIO MATEMATICO
def duplica_cliente(edad):
	#INTENTA HACER LA PETICION AL SERVICIO, INDICANDO QUE NO ESTA CONECTADO
	#EN CASO DE APARECER LA EXCEPTION
    try:
		#SE DEFINE EL CLIENTE
        dup = rospy.ServiceProxy('duplica', duplica)

		#SE HACE LA PETICION CON LA EDAD
        resp = dup(edad)

		#SE IMPRIME POR PANTALLA LA EDAD
        rospy.loginfo("El doble de la edad es: %d", resp.edadx2)


    except rospy.ServiceException as e:
        print("El nodo matematico no esta conectado")

#CALLBACK EN CASO DE RECIBIR UN MENSAJE DEL EMPAQUETADOR
def callback(data):
	#DEFINO COMO GLOBAL ALGUNA VARIABLE QUE USARÉ
    global first,start,reset

	#COMPRUEBA SI ES EL PRIMER MENSAJE QUE RECIBE, EN ESE CASO LO PUBLICA AL RELOJ
	#POR EL PUBLICADOR DE START
    if first:
        start.publish("Start")

		#SE PONE LA FLAG A FALSE PARA QUE NO VUELVA A ENTRAR
        first=False

	#LAS SIGUIENTES VECES LO HARÁ POR EL DE RESET
    else:
        reset.publish("Reset")

	#IMPRIME EL NOMBRE RECIBIDO
    rospy.loginfo("Nombre: %s" ,data.inf.nombre)

	#CREA LA CADENA DE CARÁCTERES DEL COMANDO
    scommand='espeak -ves+m3' +' "'+"Se llama: " +data.inf.nombre + '"'

	#HACE LA LLAMADA AL SISTEMA CON EL COMANDO A LANZAR, EN ESTE CASO EL SINTETIZADOR
    os.system(scommand)

	#HACE UNA PETICION AL ACTIONLIB SERVER
    action_lib_client(data.inf.nombre)

    #IMPRIME LA EDAD
    rospy.loginfo("Edad: %d" ,data.inf.edad)

	#CREA LA CADENA DE CARÁCTERES DEL COMANDO
    scommand='espeak -ves+m3' +' "'+"Tiene: " +str(data.inf.edad) + " años"+'"'

	#HACE LA LLAMADA AL SISTEMA CON EL COMANDO A LANZAR, EN ESTE CASO EL SINTETIZADOR
    os.system(scommand)

	#HACE LA LLAMADA AL SERVICIO MATEMATICO
    duplica_cliente(data.inf.edad)

	#IMPRIME LOS IDIOMAS QUE HABLA
    rospy.loginfo("Idiomas: %s" ,data.inf.idiomas)

	#CREA CON LOS IDIOMAS UNA CADENA DE TEXTO LEGIBLE, ESTO ES PARA QUE AL SINTETIZAR
	#EL TEXTO QUEDE MAS NATURAL, AÑADIENDO LA CONJUNCION "Y" ENTRE LOS DOS ULTIMOS
	#IDIOMAS DE LA LISTA Y COMAS ENTRE EL RESTO
    idioma_str=data.inf.idiomas[0]
    if len(data.inf.idiomas)>1:
        for i in range(1,len(data.inf.idiomas)):
            if i==len(data.inf.idiomas)-1:
                idioma_str=idioma_str + " y "
            else:
                idioma_str=idioma_str+ ", "
            idioma_str=idioma_str+data.inf.idiomas[i]
    #SE CREA LA CADENA COMPLETA DEL COMANDO
    scommand='espeak -ves+m3' +' "'+"Habla: " +idioma_str + '"'

	#SE LANZA EL COMANDO
    os.system(scommand)

	#SE IPRIME LA EMOCION
    rospy.loginfo("Emocion: %s",data.emocion)

	#SE CREA LA CADENA DE TEXTO DEL COMANDO CON LA EMOCION
    scommand='espeak -ves+m3' +' "'+"Se encuentra: " +data.emocion + '"'

	#SE LANZA EL COMANDO
    os.system(scommand)

	#FINALMENTE SE IMPRIME LA POSICION, EN ESTE CASO NO SE SINTETIZA
    rospy.loginfo("Posicion: X:%d    Y:%d    Z:%d",data.posicion.x ,data.posicion.y ,data.posicion.z)


#CALLBACK DEL MENSAJE DE STILL_ALIVE
def still_alive(data):
	#LO INDICA POR PANTALLA
    rospy.loginfo("--------EL NODO RELOJ SIGUE VIVO--------")

#FUNCION PRINCIPAL
def dialogo():
	#DEFINIMOS LAS VARIABLES QUE SE USARAN COMO GLOBALES
    global first,start,reset

	#SE INICIALIZA A TRUE EL FLAG DE PRIMER MENSAJE
    first=True

	#SE INICIA EL NODO
    rospy.init_node('dialogo', anonymous=True)

	#SE DEFINE LOS PUBLICADORES
    start=rospy.Publisher('start_topic', String, queue_size=1)
    reset=rospy.Publisher('reset_topic', String, queue_size=1)

	#SE DEFINEN LOS SUBSCRIPTORES
    rospy.Subscriber('user_topic', usuario, callback)
    rospy.Subscriber('still_alive', Bool, still_alive)

	#SE PONE A CORRER
    rospy.spin()

if __name__=="__main__":
	#INICIAMOS
    dialogo()

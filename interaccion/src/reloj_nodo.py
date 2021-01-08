import rospy
from std_msgs.msg import String,Bool
from datetime import datetime

#CALLBACK CUANDO RECIBE UN TOPIC DE RESET
def callbackR(data):
    #DEFINIMOS ACT COMO GLOBAL
    global act
    #DEFINIMOS ACT COMO EL TIEMPO EN EL MOMENTO QUE SE LLAMA AL CALLBACK
    act = rospy.get_rostime().secs

#CALLBACK CUANDO RECIBE UN TOPIC DE START
def callbackS(data):
    #DEFINIMOS ACT COMO GLOBAL
    global act

    #DEFINIMOS ACT COMO EL TIEMPO EN EL MOMENTO QUE SE LLAMA AL CALLBACK
    act = rospy.get_rostime().secs

    #COMENZAMOS A IMPRIMIR POR PANTALLA
    imprime()

#IMPRIME POR PANTALLA LOS CAMPOS HORA LOCAL, HORA UTC Y TIEMPO DESDE EL ULTIMO RESET/START
def imprime():
    #DEFINIMOS ACT COMO GLOBAL
    global act
    #EL RATE AL QUE QUEREMOS IMPRIMIR POR PANTALLA, EN ESTE CASO 3HZ
    r=rospy.Rate(3)
    #COMENZAMOS A IMPRIMIR
    while True:
        #EL TIEMPO ACTUAL
        now = rospy.get_rostime()
        #CONVERSION DE TIMESTAMP A UTC DE LA HORA UTC Y LA ACTUAL
        horautc=datetime.utcfromtimestamp(now.secs).strftime('%Hh:%Mm:%Ss')
        hora=datetime.utcfromtimestamp(now.secs+3600).strftime('%Hh:%Mm:%Ss')
        #IMPRIMIMOS
        rospy.loginfo("La hora UTC es: %s     La hora LOCAL es: %s    Segundos desde el ultimo reset/start es: %i" , horautc,hora,now.secs-act)
        r.sleep()

#CALLBACK CUANDO RECIBE EL STILL_ALIVE
def still_alive(event):
    #DEFINIMOS EL PUBLICADOR
    global pub
    #PUBLICAMOS
    pub.publish(True)

#FUNCION PRINCIPAL
def reloj():
    #DEFINIMOS EL PUBLICADOR COMO GLOBAL
    global pub
    #INICIAMOS EL NODO
    rospy.init_node('reloj', anonymous=True)
    #DEFINIMOS EL PUBLICADOR
    pub = rospy.Publisher('still_alive', Bool,queue_size=1)
    #DEFINIMOS LOS SUBSCRIPTORES
    rospy.Subscriber('reset_topic', String, callbackR)
    rospy.Subscriber('start_topic', String, callbackS)
    #DEFINIMOS EL TIMER QUE LANZA LA FUNCION STILL_ALIVE CADA 60S
    rospy.Timer(rospy.Duration(60), still_alive)
    #LO PONEMOS A CORRER
    rospy.spin()

if __name__=='__main__':
    #LO INICIALIZAMOS 
    reloj()

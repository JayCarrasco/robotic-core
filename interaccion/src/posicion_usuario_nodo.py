# encoding: utf-8

#IMPORTAMOS ROSPY Y EL MENSAJE
import rospy
from interaccion.msg import pos_usuario

#FUNCION QUE PIDE LA POSICION DEL USUARIO POR TECLADO
def get_pos():
    #INICIAMOS EL MENSAJE
    pos=pos_usuario()
    #VAMOS PIDIENDO LAS COORDENADAS
    #SI AL INTRODUCIR UNA COORDENADA, ESTA CONTIENE UN CARÁCTER ALFABETICO,
    #LO INDICA Y VUELVE A PEDIR LA COORDENADA
    rospy.loginfo("Introduce la posicion X: ")
    x=input()
    if any(c.isalpha() for c in x):
        while any(c.isalpha() for c in x):
            rospy.loginfo("Debes introducir un numero entero para X: ")
            x=input()

    rospy.loginfo("Introduce la posicion Y: ")
    y=input()
    if any(c.isalpha() for c in y):
        while any(c.isalpha() for c in y):
            rospy.loginfo("Debes introducir un numero entero para Y: ")
            y=input()
    rospy.loginfo("Introduce la posicion Z: ")
    z=input()
    if any(c.isalpha() for c in z):
        while any(c.isalpha() for c in z):
            rospy.loginfo("Debes introducir un numero entero para Z: ")
            z=input()
    #ESTABLECEMOS LAS POSICIONES INTRODUCIDAS EN EL MENSAJE
    pos.x=int(x)
    pos.y=int(y)
    pos.z=int(z)
    #DEVOLVEMOS LA POSICION
    return pos

#UNA VEZ SE HA ENVIADO, IMPRIMIMOS UN RESUMEN DE LA POSICION ENVIADA
def print_pos(x,y,z):
    rospy.loginfo("Posicion X: %d",x)
    rospy.loginfo("Posicion Y: %d",y)
    rospy.loginfo("Posicion Z: %d",z)

#FUNCION PRIMCIPAL
def posicion_usuario_nodo():
    #DEFINIMOS EL PUBLICADOR
    pub = rospy.Publisher('pos_usuario_topic', pos_usuario,queue_size=1)
    #INCIAMOS EL NODO
    rospy.init_node('posicion', anonymous=True)
    #VAMOS PIDIENDO INFORMACION POR TECLADO INDEFINIDAMENTE
    rate = rospy.Rate(1)
    while not rospy.is_shutdown():
        posicion=get_pos()
        print_pos(posicion.x,posicion.y,posicion.z)
        #PUBLICAMOS EL MENSAJE
        pub.publish(posicion)
        rate.sleep()

#PONEMOS TODO A CORRER
if __name__=="__main__":
    try:
        posicion_usuario_nodo()
    except rospy.ROSInterruptException:
        pass

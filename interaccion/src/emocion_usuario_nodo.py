
#CARGAMOS EL ROSPY Y EL MENSAJE
import rospy
#from trabajo.msg import emocion_usuario
from std_msgs.msg import String
#FUNCION PRINCIPAL
def emocion_usuario_nodo():
    #DEFINIMOS EL PUBLICADOR
    pub = rospy.Publisher('emocion_topic', String, queue_size=1)
    #INICIAMOSEL NODO
    rospy.init_node('emocion', anonymous=True)

    rate = rospy.Rate(1)
    while not rospy.is_shutdown():

        rospy.loginfo("Introduce la emocion: ")
        #INICIAMOS EL MENSAJE
        #emocion=emocion_usuario()
        #ESTABLECEMOS EL MENSAJE A ENVIAR A LO QUE EL USUARIO INTRODUZCA POR TECLADO
        emocion=str(input())
        #PIBLICAMOS
        pub.publish(emocion)

        rate.sleep()
if __name__=='__main__':
    try:
        emocion_usuario_nodo()
    except rospy.ROSInterruptException:
        pass

#CARGAMOS ROSPY Y EL SERVICIO
import rospy
from trabajo.srv import multiplicador

#DUPLICA EL VALOR RECIBIDO
def duplicador(req):
    valor=req.edad*2
    return valor


def servicio_servidor():
    #INICIAMOS EL NODO
    rospy.init_node('matematico_nodo')

    #INICIAMOS EL SERVICIO
    s = rospy.Service('multiplicador', multiplicador,duplicador)

    #LO DEJAMOS A LA ESPERA DE PETICIONES
    rospy.spin()


if __name__ == '__main__':
    #SE INICIALIZA
    servicio_servidor()

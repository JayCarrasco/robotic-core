#CARGAMOS ROSPY Y LOS MENSAJES
import rospy
from trabajo.msg import emocion_usuario, inf_personal_usuario,pos_usuario,usuario
from std_msgs.msg import Bool,String

#CALLBACK QUE LLAMA CUANDO LLEGA LA INFORMACION PERSONAL
def callback_uno(data):
    #IMPRIMIMOS QUE HA LLEGADO LA INFORMACION, PARA TENER UN CONTROL DEL PASO DE MENSAJES MAS DIRECTO
    rospy.loginfo("Llega la informacion personal")
    #DEFINIMOS VARIABLES GLOBALES QUE NECESITAMOS
    global flag_enviado,flag_info,usuarioT,lista_nombre,lista_edad,lista_idiomas

    #AÑADIMOS A LAS LISTAS LA INFORMACION QUE HA LLEGADO
    lista_nombre.append(str(data.nombre))
    lista_edad.append(int(data.edad))
    lista_idiomas.append(list(data.idiomas))

    #ESTABLECEMOS LA INFORMACION A ENVIAR COMO LA INFORMACION EN LA PRIMERA POSICION DE LA LISTA
    usuarioT.inf.nombre=lista_nombre[0]
    usuarioT.inf.edad=lista_edad[0]
    usuarioT.inf.idiomas=lista_idiomas[0]

    #INDICAMOS QUE HEMOS CARGADO LA INFORMACION
    flag_info=True

#CALLBACK QUE LLAMA CUANDO LLEGA LA POSICION
def callback_dos(data):
    #IMPRIMIMOS QUE HA LLEGADO LA POSICION, PARA TENER UN CONTROL DEL PASO DE MENSAJES MAS DIRECTO
    rospy.loginfo("llega posicion")

    #DEFINIMOS VARIABLES GLOBALES QUE NECESITAMOS
    global flag_enviado,flag_pos,usuarioT,lista_x,lista_y,lista_z

    #AÑADIMOS A LAS LISTAS LA INFORMACION QUE HA LLEGADO
    lista_x.append(int(data.x))
    lista_y.append(int(data.y))
    lista_z.append(int(data.z))

    #ESTABLECEMOS LA INFORMACION A ENVIAR COMO LA INFORMACION EN LA PRIMERA POSICION DE LA LISTA
    usuarioT.posicion.x=lista_x[0]
    usuarioT.posicion.y=lista_y[0]
    usuarioT.posicion.z=lista_z[0]

    #INDICAMOS QUE HEMOS CARGADO LA INFORMACION
    flag_pos=True

#CALLBACK QUE LLAMA CUANDO LLEGA LA EMOCION DE LA PERSONA
def callback_tres(data):
    #IMPRIMIMOS QUE HA LLEGADO LA EMOCION, PARA TENER UN CONTROL DEL PASO DE MENSAJES MAS DIRECTO
    rospy.loginfo("llega emocion")

    #DEFINIMOS VARIABLES GLOBALES QUE NECESITAMOS
    global flag_enviado,flag_emo,usuarioT,lista_emo

    #AÑADIMOS A LAS LISTAS LA INFORMACION QUE HA LLEGADO
    lista_emo.append(str(data))

    #ESTABLECEMOS LA INFORMACION A ENVIAR COMO LA INFORMACION EN LA PRIMERA POSICION DE LA LISTA
    usuarioT.emocion=lista_emo[0]

    #INDICAMOS QUE HEMOS CARGADO LA INFORMACION
    flag_emo=True



def listener():
    #INICIALIZAMOS EL NODO
    rospy.init_node('empaquetador', anonymous=True)
    #DEFINIMOS LOS SUBSCRIPTORES
    rospy.Subscriber('inf_pers_topic', inf_personal_usuario,callback_uno)
    rospy.Subscriber('pos_usuario_topic', pos_usuario,callback_dos)
    rospy.Subscriber('emocion_topic', String, callback_tres)
    #DEFINIMOS LAS VARIABLES GLOBALES QUE VAMOS USANDO
    global lista_nombre,flag_enviado,lista_edad,lista_idiomas,lista_x,lista_y,lista_z,lista_emo,flag_emo,flag_pos,flag_info



if __name__ == '__main__':
    #DEFINIMOS COMO GLOBALES LAS VARIABLES QUE VAMOS USANDO
    global lista_nombre,lista_edad,lista_idiomas,lista_x,lista_y,lista_z,lista_emo
    #INICIALIZAMOS LAS VARIABLES QUE VAMOS A UAR
    lista_nombre=[]
    lista_edad=[]
    lista_idiomas=[]
    lista_x=[]
    lista_y=[]
    lista_z=[]
    lista_emo=[]
    flag_emo=False
    flag_pos=False
    flag_info=False
    flag_enviado=False
    #INICIAMOS EL MENSAJE QUE SE VA A ENVIAR, DEL TIPO usuario
    usuarioT=usuario()  
    #INICIAMOS LA ESCUCHA
    listener()
    #INICIAMOS EL PUBLICADOR
    pub = rospy.Publisher('user_topic', usuario,queue_size=1)

    while not rospy.is_shutdown():
        #SI SE RECIBE LA INFORMACION DE LOS 3 NODOS
        if flag_emo and flag_info and flag_pos:

            try:
                #ENVIA LA INFORMACION Y RESETEA LAS FLAGS
                rospy.loginfo("enviando")
                flag_enviado=True
                if len(lista_emo)<=1:
                   flag_emo=False
                if len(lista_z)<=1:
                    flag_pos=False
                if len(lista_nombre)<=1:
                    flag_info=False

                pub.publish(usuarioT)

                #BORRAMOS LA INFORMACION DE LA PRIMERA POSICION DE LAS LISTAS, QUE ES LA QUE YA HEMOS ENVIADO
                lista_x.pop(0)
                lista_y.pop(0)
                lista_z.pop(0)
                lista_emo.pop(0)
                lista_nombre.pop(0)
                lista_edad.pop(0)
                lista_idiomas.pop(0)
                if len(lista_x)>0:
                    usuarioT.x=lista_x[0]
                if len(lista_y)>0:
                    usuarioT.y=lista_y[0]
                if len(lista_z)>0:
                    usuarioT.z=lista_z[0]
                if len(lista_nombre)>0:
                    usuarioT.nombre=lista_nombre[0]
                if len(lista_edad)>0:
                    usuarioT.edad=lista_edad[0]
                if len(lista_emo)>0:
                    usuarioT.emocion=lista_emo[0]
                if len(lista_idiomas)>0:
                    usuarioT.idiomas=lista_idiomas[0]

            except rospy.ROSInterruptException:
                pass

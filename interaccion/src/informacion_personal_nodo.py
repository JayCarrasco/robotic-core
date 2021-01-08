#INPORTAMOS ROSPY Y EL MENSAJE
import rospy
from trabajo.msg import inf_personal_usuario


#FUNCION ENCARGADA DE PEDIR LA INFORMACION POR TECLADO
def get_info():
    #INICIAMOS EL MENSAJE
    personaMsg=inf_personal_usuario()
    #PEDIMOS EL NOMBRE
    rospy.loginfo("Introduce el nombre: ")
    personaMsg.nombre=input()
    #PEDIMOS LA EDAD
    rospy.loginfo("Introduce la edad ")
    edad=input()
    #COMPROBAMOS SI TIENE ALGUN CARÁCTER NO NUMÉRICO Y SI LO CONTIENE, INDICAMOS
    #QUE VUELVA A INTRODUCIRLO
    if any(c.isalpha() for c in edad):
        while any(c.isalpha() for c in edad):
            rospy.loginfo("La edad debe ser un numero entero: ")
            edad=input()
    personaMsg.edad=int(edad)
    #PEDIMOS EL NUMERO DE INDIOMAS
    rospy.loginfo("Introduce el numero de idiomas: ")
    num_idiomas=input()
    #IGUAL QUE CON LA EDAD, SI NO ES UN ENTERO VUELVE A PEDIRLO
    if any(c.isalpha() for c in num_idiomas):
        while any(c.isalpha() for c in num_idiomas):
            rospy.loginfo("Debe ser una cantidad entera: ")
            num_idiomas=input()
    #UNA VEZ SE INTRODUCE EL VALOR CORRECTO, PIDE LOS IDIOMAS Y LOS ESTABLECE
    for i in range(int(num_idiomas)):
        rospy.loginfo("Introduce el idioma %d: ",i+1)
        idioma=input()
        personaMsg.idiomas.append(idioma)
    #DEVOLVEMOS EL MENSAJE
    return personaMsg

#UNA VEZ HA ENVIADO TODA LA INFORMACION, SACA UN RESUMEN DE LO QUE HA ENVIADO
def print_persona(persona):
    rospy.loginfo("Nombre enviado: %s", persona.nombre)
    rospy.loginfo("Edad enviada: %s ", persona.edad)
    for i in range(len(persona.idiomas)):
        rospy.loginfo("Idioma %i: %s",i+1,persona.idiomas[i])
def informacion_personal_nodo():
    #DEFINIMOS EL PUBLICADOR
    pub = rospy.Publisher('inf_pers_topic', inf_personal_usuario,queue_size=1)
    #INICIAMOS EL NODO
    rospy.init_node('persona', anonymous=True)
    rate = rospy.Rate(1)
    while not rospy.is_shutdown():
        #VAMOS PIDIENDO INFORMACION HASTA QUE EL NODO MUERE
        persona=get_info()
        print_persona(persona)
        pub.publish(persona)
        rate.sleep()

if __name__=="__main__":
    #SE INICIA TODO
    try:
        informacion_personal_nodo()
    except rospy.ROSInterruptException:
        pass

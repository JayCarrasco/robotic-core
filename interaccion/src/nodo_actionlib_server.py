#SE IMPORTAN LAS LIBRERIAS QUE SE VAN A USAR
import rospy
import actionlib
from trabajo.msg import testAction,testResult,testFeedback
import trabajo.msg
import os

class test_lib(object):
    #SE DEFINEN LAS VARIABLES PRIVADAS COMO EL FEEDBACK Y EL RESULT, AUNQUE EN
    #ESTE CASO, DEBIDO A LA FUNCION DEL SERVIDOR, QUE ES DELETREAR, NO SON VARIBALES QUE TENGAN
    #UNA FUNCION DETERMINANTE
    _feedback = testFeedback()
    _result = testResult()

    #CONSTRUCTOR
    def __init__(self):
        #SE DEFINE EL SERVIDOR Y SE LANZA
        self._as = actionlib.SimpleActionServer('deletrea', testAction, execute_cb=self.execute_cb, auto_start = False)
        self._as.start()

    #CALLBACK
    def execute_cb(self, goal):


        #RATE DE 1HZ
        r = rospy.Rate(1)
        #SE INICIA SUCCESS A TRUE
        success = True


        #SE INICIA EL FEEDBACK A UNA CADENA VACIA
        self._feedback.infoFeedback = []


        #SE INDICA EL NOMBRE A DELETREAR
        rospy.loginfo('Deletreando el nombre: %s',goal.goal)

        #COMANDO A LANZAR
        scommand='espeak -ves+m3 deletreado: '

        #SE LANZA
        os.system(scommand)

        #COMENZAMOS A DELETREAR
        for i in range(len(goal.goal)):

        # COMPRUEBA QUE NO SE HAYA PEDIDO EL CONTROL
            if self._as.is_preempt_requested():
                rospy.loginfo('Preempted')
                self._as.set_preempted()
                success = False
                break
            #CREA EL COMANDO CON CADA LETRA
            scommand='espeak -ves+m3 '+goal.goal[i]
            #LANZA EL COMANDO Y SINTETIZA LA LETRA
            os.system(scommand)

            #METEMOS LA LETRA EN LA LISTA EL FEEDBACK
            self._feedback.infoFeedback.append(goal.goal[i])

            # PUBLICAMOS EL FEEDBACK
            self._as.publish_feedback(self._feedback)

            # ESPERAMOS 1 SEGUNDO ANTES DE HACER OTRA ITERACION, PARA QUE SE
            #SINTETICE CORRECTAMENTE
            r.sleep()

         #CUANDO ACABE, MIENTRAS NO SE HAYA PEDIDO EL CONTROL
        if success:
            #ESTABLECE COMO RESULTADO LA CADENA DEL FEEDBACK
            self._result.result = self._feedback.infoFeedback

            #INDICA QUE HA TENIDO EXITO
            rospy.loginfo('Succeeded')

            #ESTABLECE EL ESTADO DEL GOAL ACTUAL COMO EXITO
            self._as.set_succeeded(self._result)

if __name__ == '__main__':
    #SE INICIA EL NODO
    rospy.init_node('deletrea')

    #SE LANZA EL SERVIDOR
    server = test_lib()

    #SE DEJA A LA ESPERA
    rospy.spin()

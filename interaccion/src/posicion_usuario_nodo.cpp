#include "ros/ros.h"
#include "interaccion/pos_usuario.h"

using namespace std;

/**
* Este nodo llamado informacion_personal_nodo emite mensajes "inf_pers_topic"
del tipo interaccion::pos_usuario
*/

int main(int argc, char **argv)
{
    ros::init(argc, argv, "posicion_usuario_nodo");
    ros::NodeHandle nodoPosicionUsuario;

    //Se crea un objeto tipo nodo
    ROS_INFO("posicion_usuario_nodo creado y registrado");

    //Es necesario advertir el tipo de mensaje a enviar y como le hemos llamado (el topic)
    ros::Publisher publicadorPosicion = nodoPosicionUsuario.advertise<interaccion::pos_usuario>("pos_usuario_topic", 0);

    ros::Duration seconds_sleep(1);

    //Ejecuta hasta recibir Ctrl+c
    while(ros::ok())
    {
        //instanciamos un mensaje que queremos enviar
        interaccion::pos_usuario mensajePosicion;

        //en el mensaje enviamos el número de veces que se ha iterado en este bucle
        cout<< "Por favor, ingrese la posicion en x: "<<"\n";
        cin>>mensajePosicion.x;
        cout<< "Por favor, ingrese la posicion en y: "<<"\n";
        cin>>mensajePosicion.y;
        cout<< "Por favor, ingrese la posicion en z: "<<"\n";
        cin>>mensajePosicion.z;

        //se publica el mensaje
        publicadorPosicion.publish(mensajePosicion);

        //en este programa no es necesario spinOnce, pero si tuviera una funcion de callback es imprescindible para que se ejecute
        ros::spinOnce();
        ROS_DEBUG ("Se duerme el nodo emisor durante un segundo");

        //dormimos el nodo durante un tiempo
        seconds_sleep.sleep();
    }
}
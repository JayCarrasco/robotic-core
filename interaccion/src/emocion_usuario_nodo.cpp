//Se incluyen las cabeceras
#include "ros/ros.h"
#include "std_msgs/String.h"
#include <string>

//Declaracion del namespace std
using namespace std;

//Funcion principal
int main(int argc, char **argv)
{   
    //Se crea el nodo emocion_usuario_nodo y el handle nodoEmocionUsuario
    ros::init(argc, argv, "emocion_usuario_nodo");
    ros::NodeHandle nodoEmocionUsuario;

    //Se crea un objeto tipo nodo
    ROS_INFO("emocion_usuario_nodo creado y registrado");

    //Es necesario advertir el tipo de mensaje a enviar y como le hemos llamado (emocion_topic)
    ros::Publisher publicadorEmociones = nodoEmocionUsuario.advertise<std_msgs::String>("emocion_topic", 0);

    //frecuencia de ejecucion del bucle
    ros::Duration seconds_sleep(1);

    //Ejecuta hasta recibir Ctrl+c
    while(ros::ok())
    {   
        //Se instancia el mensaje a enviar
        std_msgs::String mensajeEmocion;
        stringstream ss;
        string emocion;

        //Se pide la emoción a enviar
        cout<<"Por favor, ingrese la emocion: \n";
        cin>>emocion;

        ss<<emocion;

        mensajeEmocion.data = ss.str();

        //Se publica el mensaje con la emocion
        publicadorEmociones.publish(mensajeEmocion);

        ros::spinOnce();
        ROS_DEBUG("Se duerme el nodo emisor un segundo");
        seconds_sleep.sleep();
    }
    
    return 0;
}

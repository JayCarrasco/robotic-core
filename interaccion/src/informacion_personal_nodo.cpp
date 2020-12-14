#include "ros/ros.h"
#include "interaccion/inf_personal_usuario.h"
#include <string>

using namespace std;

/**
* Este nodo llamado informacion_personal_nodo emite mensajes "inf_pers_topic"
del tipo interaccion::inf_personal_usuario
*/

int main(int argc, char **argv) {
    ros::init(argc, argv, "informacion_personal_nodo"); //registra el nombre del nodo
    ros::NodeHandle nodoInfPers;

    //Creamos un objeto nodo
    ROS_INFO("informacion_personal_nodo creado y registrado"); //to screen and file
    //es necesario "advertir" el tipo de mensaje a enviar y como lo hemos llamado (el topic).
    ros::Publisher publicadorMensajes = nodoInfPers.advertise<interaccion::inf_personal_usuario>("inf_pers_topic",0);

    //tiempo a dormir en cada iteracción
    ros::Duration seconds_sleep(1);

    //ejecuta constantemente hasta recibir un Ctr+C
    int contador = 0;
    while (ros::ok()){
        //int num_idiomas = 0;
        //string[] idiomas0 = {};

        //instanciamos un mensaje que queremos enviar
        interaccion::inf_personal_usuario mensajeAEnviar;

        //en el mensaje enviamos el número de veces que se ha iterado en este bucle
        cout<< "Por favor, ingrese el nombre: "<<"\n";
        cin>>mensajeAEnviar.nombre;
        cout<< "Por favor, ingrese la edad: "<<"\n";
        cin>>mensajeAEnviar.edad;
        /*
	cout<<"Introduzca el numero de idiomas que sepa: "<<"\n";
        cin>>num_idiomas;
        for (int i = 0; i < num_idiomas; i++) {
          cout<< "Por favor, ingrese el idioma "<< i <<": "<<"\n";
          cin>>idiomas0[i];
        }

        cout<< "Los idiomas registrados son: "<< idiomas0 <<"\n";
	*/
        mensajeAEnviar.idiomas = {"ingles", "espanyol"};


        //se publica el mensaje
        publicadorMensajes.publish(mensajeAEnviar);

        //en este programa no es necesario spinOnce, pero si tuviera una funcion de callback es imprescindible para que se ejecute
        ros::spinOnce();
        ROS_DEBUG ("Se duerme el nodo emisor durante un segundo");

        //dormimos el nodo durante un tiempo
        seconds_sleep.sleep();

    }
}

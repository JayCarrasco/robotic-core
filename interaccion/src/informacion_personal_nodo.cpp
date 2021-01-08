/**
* Este nodo llamado informacion_personal_nodo emite mensajes "inf_pers_topic"
del tipo interaccion::inf_personal_usuario
*/

//Se incluyen las cabeceras
#include "ros/ros.h"
#include "interaccion/inf_personal_usuario.h"
#include <string>

//Se declaran los namespaces
using namespace std;

//funcion principal
int main(int argc, char **argv) {
    //Se crea el nodo informacion_personal_nodo y el handle nodoInfPers
    ros::init(argc, argv, "informacion_personal_nodo"); //registra el nombre del nodo
    ros::NodeHandle nodoInfPers;

    ROS_INFO("informacion_personal_nodo creado y registrado"); //to screen and file

    //es necesario "advertir" el tipo de mensaje a enviar, que tiene topic inf_pers_topic
    ros::Publisher publicadorMensajes = nodoInfPers.advertise<interaccion::inf_personal_usuario>("inf_pers_topic",0);
    
    //tiempo a dormir en cada iteracción
    ros::Duration seconds_sleep(1);

    //ejecuta constantemente hasta recibir un Ctr+C

    while (ros::ok()){
        //Se inicializa el numero de idiomas
        int num_idiomas = 0;
        std::vector<std::string> idiomas_array;

        //instanciamos un mensaje que queremos enviar
        interaccion::inf_personal_usuario mensajeAEnviar;

        //Se introduce nombre y edad
        cout<< "Por favor, ingrese el nombre: "<<"\n";
        cin>>mensajeAEnviar.nombre;
        cout<< "Por favor, ingrese la edad: "<<"\n";
        cin>>mensajeAEnviar.edad;

        //Numero de idiomas
	    cout<<"Introduzca el numero de idiomas que sepa: "<<"\n";
        cin>>num_idiomas;
        string idioma[num_idiomas];
        
        //Idiomas que sabe
        for (int i = 0; i < num_idiomas; i++) {
          cout<< "Por favor, ingrese el idioma "<< i <<": "<<"\n";
          cin>>idioma[i];
          idiomas_array.push_back(idioma[i]);
        }
        
        //Se introduce el array de idiomas en el mensaje
        mensajeAEnviar.idiomas = idiomas_array;


        //se publica el mensaje
        publicadorMensajes.publish(mensajeAEnviar);

        //en este programa no es necesario spinOnce, pero si tuviera una funcion de callback es imprescindible para que se ejecute
        ros::spinOnce();
        ROS_DEBUG ("Se duerme el nodo emisor durante un segundo");

        //dormimos el nodo durante un tiempo
        seconds_sleep.sleep();

    }
}

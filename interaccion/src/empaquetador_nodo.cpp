/**
 * Se implementa un nodo que espera recibir mensajes cuyo topic es "inf_pers_topic" del tipo interaccion::inf_personal_usuario.
 * Muestra en pantalla este mensaje recibido
 */

//Se incluyen las cabeceras
#include "ros/ros.h"
#include "interaccion/inf_personal_usuario.h"
#include "interaccion/usuario.h"
#include "std_msgs/String.h"
#include <string>

//Se declara el namespace std
using namespace std;

//Estructura para la informacion personal
struct {
    string nombre;
    int edad;
    std::vector<std::string> idiomas;
} infPersonal;


//Estructura para la posicion
struct {
    int x;
    int y;
    int z;
} posicion;

//Algunos bools de confirmacion de mensaje
bool confirmacionInfPersonal = false;
bool confirmacionEmocion = false;
bool confirmacionPosicion = false;

//Se declara el published como variable global
ros::Publisher publicadorEmpaquetador;

//Se instancia el mensaje a publicar como variable global
interaccion::usuario mensajeEmpaquetador;

/**
* Esta función muestra por pantalla el mensaje recibido que es de tipo inf_personal_usuario
*/
void funcionCallback(const interaccion::inf_personal_usuario::ConstPtr& msg){
 ROS_INFO("El nombre es: %s", msg->nombre.c_str());
 ROS_INFO("La edad es: %d", msg->edad);
 for (int i = 0; i < msg->idiomas.size(); i++) {
   ROS_INFO("Los idiomas que se son: %s", msg->idiomas[i].c_str());
 }
 
 //Se confirma la informacion personal
 confirmacionInfPersonal = true;
 ROS_INFO("confirmo info personal: %d", confirmacionInfPersonal);

 /*Se introduce la informacion personal recibida en la estructura infPersonal,
 y en el mensajeEmpaquetador*/
 mensajeEmpaquetador.infPersonal.edad = msg->edad;
 mensajeEmpaquetador.infPersonal.nombre = msg->nombre;
 mensajeEmpaquetador.infPersonal.idiomas = msg->idiomas;
}

/**
* Esta función muestra por pantalla el mensaje recibido que es de tipo String
*/
void funcionCallback2(const std_msgs::String::ConstPtr& msg){
 ROS_INFO("La emocion es: %s", msg->data.c_str());
 
 //Se confirma que llega el mensaje de la emocion
 confirmacionEmocion = true;
 ROS_INFO("confirmo info emocion: %d", confirmacionEmocion);
 
 //Se introduce el mensaje en el mensajeEmpaquetador
 mensajeEmpaquetador.emocion = msg->data.c_str();
}

/**
* Esta función muestra por pantalla el mensaje recibido que es de tipo pos_usuario
*/
void funcionCallback3(const interaccion::pos_usuario::ConstPtr& msg){
 ROS_INFO("La posicion en x es: %d", msg->x);
 ROS_INFO("La posicion en y es: %d", msg->y);
 ROS_INFO("La posicion en z es: %d", msg->z);
 
 //Se confirma que ha llegado el mensaje de la posicion
 confirmacionPosicion = true;
 ROS_INFO("confirmo info posicion: %d", confirmacionPosicion);
 
 /*Se introduce el mensaje recibido en la estructura posicion,
 y de ahi al mensajeEmpaquetador*/
 mensajeEmpaquetador.posicion.x = msg->x;
 mensajeEmpaquetador.posicion.y = msg->y;
 mensajeEmpaquetador.posicion.z = msg->z;
}

//Funcion principal
int main(int argc, char **argv){

 //registra el nombre del nodo: empaquetador_nodo y el handle empaquetadorNodo
 ros::init(argc, argv, "empaquetador_nodo");

 ros::NodeHandle empaquetadorNodo;

 //Creamos un objeto nodo
 ROS_INFO("empaquetador_nodo creado y registrado"); //muestra en pantalla

 //es necesario "advertir" el tipo de mensaje a enviar con el topic user_topic
 publicadorEmpaquetador = empaquetadorNodo.advertise<interaccion::usuario>("user_topic",0);

 //si recibimos el mensaje cuyo topic es: "inf_pers_topic" llamamos a la función manejadora: funcionCallback
 ros::Subscriber subscriptor = empaquetadorNodo.subscribe("inf_pers_topic", 0, funcionCallback);

 //si recibimos el mensaje cuyo topic es: "emocion_topic" llamamos a la función manejadora functionCallback2
 ros::Subscriber subscriptor2 = empaquetadorNodo.subscribe("emocion_topic", 0, funcionCallback2);

 //si recibimos el mensaje cuyo topic es: "pos_usuario_topic" llamamos a la función manejadora functionCallback3
 ros::Subscriber subscriptor3 = empaquetadorNodo.subscribe("pos_usuario_topic", 0, funcionCallback3);

 while (ros::ok()){
    //Cuando haya llegado toda la informacion, se publica el mensaje
    if (confirmacionEmocion == true and confirmacionInfPersonal == true and confirmacionPosicion == true)
     {
        publicadorEmpaquetador.publish(mensajeEmpaquetador);

        //Se reseteran para empaquetar nueva informacion
        confirmacionEmocion = false;
        confirmacionInfPersonal = false;
        confirmacionPosicion = false;
    }
    ros::spinOnce();
 }
}

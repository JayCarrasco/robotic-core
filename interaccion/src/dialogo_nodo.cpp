#include "ros/ros.h"
#include "interaccion/usuario.h"
#include "interaccion/multiplicador.h"
#include "std_msgs/String.h"
#include "std_msgs/Bool.h"
#include <string>

/**
 * Se implementa un nodo que espera recibir mensajes cuyo topic es "user_topic" del tipo interaccion::usuario.
 * Muestra en pantalla este mensaje recibido
 */

//Muestra que le han llegado todos los datos
bool confirmarStart = false;
bool confirmarReset = false;

//Se pone a true tras enviar el primer mensaje
bool starting = false;

//Se crean srv y client como variables globales
 interaccion::multiplicador srv;
 ros::ServiceClient client;


/**
* Esta función muestra por pantalla el mensaje recibido desde el nodo empaquetador
*/
void funcionCallback(const interaccion::usuario::ConstPtr& msg){
 ROS_INFO("He recibido un mensaje de test con el nombre: %s", msg->infPersonal.nombre.c_str());;
 ROS_INFO("He recibido un mensaje de test con la edad: %d", msg->infPersonal.edad);
 for (int i = 0; i < msg->infPersonal.idiomas.size(); i++) {
   ROS_INFO("He recibido un mensaje de test con los idiomas: %s", msg->infPersonal.idiomas[i].c_str());
 }
 ROS_INFO("He recibido un mensaje de test con la emocion: %s", msg->emocion.c_str());
 ROS_INFO("He recibido un mensaje de test con la posicion en x: %d", msg->posicion.x);
 ROS_INFO("He recibido un mensaje de test con la posicion en y: %d", msg->posicion.y);
 ROS_INFO("He recibido un mensaje de test con la posicion en z: %d", msg->posicion.z);

  srv.request.entrada = msg->infPersonal.edad; //Se quiere multiplicar la edad
 if (client.call(srv)){
   ROS_INFO("Respuesta del servicio: %d", (int)srv.response.resultado);
 }else{
   ROS_ERROR("Fallo al llamar al servicio: nombre_servicio");
 }

 if (starting == false) {
 	confirmarStart = true;
 } else {
 	confirmarReset = true;
 }

}

void functionCallback2(const std_msgs::Bool::ConstPtr& msg){
	ROS_INFO("He recibido un mensaje con la info %s", msg ? "true" : "false");
}

int main(int argc, char **argv){
 //registra el nombre del nodo: nodo_receptor
 ros::init(argc, argv, "dialogo_nodo");
 ros::NodeHandle nodoDialogo;
 ROS_INFO("dialogo_nodo creado y registrado"); //muestra en pantalla

 //si recibimos el mensaje cuyo topic es: "mensajeTest_topic" llamamos a la función manejadora: funcionCallback
 ros::Subscriber subscriptorDialogo = nodoDialogo.subscribe("user_topic", 0, funcionCallback);

 ros::Subscriber subscriptorReloj = nodoDialogo.subscribe("still_alive", 0, functionCallback2);

  //vamos a invocar el servicio llamado Multiplicador
 client = nodoDialogo.serviceClient<interaccion::multiplicador>("multiplicador");

 //Se publica el mensaje start
 ros::Publisher relojStart = nodoDialogo.advertise<std_msgs::String>("start_topic",0);

  //Se publica el mensaje reset
 ros::Publisher relojReset = nodoDialogo.advertise<std_msgs::String>("reset_topic",0);
 
 while (ros::ok()){
	 if (confirmarStart == true){
	 	std_msgs::String mensajeStart;
	 	std::string start = "start";
	 	mensajeStart.data = start;

	 	relojStart.publish(mensajeStart);

	 	confirmarStart = false;
	 	starting = true;
	 }

 	 if (confirmarReset == true){
 		std_msgs::String mensajeReset;
 		std::string reset = "reset";
 		mensajeReset.data = reset;

 		relojReset.publish(mensajeReset);

  		confirmarReset = false;
	 }

	 ros::spinOnce();
	}

 /** Loop infinito para que no finalice la ejecución del nodo y siempre se pueda llamar al callback */
 //ros::spin();
 return 0;
}

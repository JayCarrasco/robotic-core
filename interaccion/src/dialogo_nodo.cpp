//Se introducen las cabeceras
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

//Declaracion de las variables de comando de voz
std::string text;
std::string command;

//Se crean srv y client como variables globales
interaccion::multiplicador srv;
ros::ServiceClient client;

//Informacion a sintetizar por voz
std::string name;
std::string age;
std::string emotion;
std::string xposition;
std::string yposition;
std::string zposition;
std::string language;

/**
* Esta función muestra por pantalla el mensaje recibido desde el nodo empaquetador
*/
void functionCallback(const interaccion::usuario::ConstPtr& msg){
 ROS_INFO("El nombre es: %s", msg->infPersonal.nombre.c_str());;
 ROS_INFO("La edad es: %d", msg->infPersonal.edad);
 for (int i = 0; i < msg->infPersonal.idiomas.size(); i++) {
   ROS_INFO("Los idiomas que se son: %s", msg->infPersonal.idiomas[i].c_str());
 }
 ROS_INFO("La emocion es: %s", msg->emocion.c_str());
 ROS_INFO("La posicion en x es: %d", msg->posicion.x);
 ROS_INFO("La posicion en y es: %d", msg->posicion.y);
 ROS_INFO("La posicion en z es: %d", msg->posicion.z);

 srv.request.entrada = msg->infPersonal.edad; //Se quiere multiplicar la edad
 if (client.call(srv)){
   ROS_INFO("La edad multiplicada por dos es: %d", (int)srv.response.resultado);
 }else{
   ROS_ERROR("Fallo al llamar al servicio: multiplicador.srv");
 }
 
 //Sintetizador de voz
 name = msg->infPersonal.nombre.c_str();
 age = std::to_string(msg->infPersonal.edad);
 emotion = msg->emocion.c_str();
 xposition = std::to_string(msg->posicion.x);
 yposition = std::to_string(msg->posicion.y);
 zposition = std::to_string(msg->posicion.z);
 
 //Los datos son sintetizados por voz de manera ordenada
 command = "espeak -v es \"" "Mi nombre es "+name+"y tengo"+age+"anyos. Mi estado de animo es"+emotion+" \"";
 system(command.c_str());
 
 command = "espeak -v es \"" "Mi posicion en coordenadas cartesinas es "+xposition+" "+yposition+" "+zposition+" \"";
 system(command.c_str());

 command = "espeak -v es \"" "Además, hablo los siguientes idiomas" " \"";
 system(command.c_str());

 for (int i = 0; i < msg->infPersonal.idiomas.size(); i++) {
   language = msg->infPersonal.idiomas[i].c_str();
   command = "espeak -v es \"" +language+ " \"";
   system(command.c_str());
 }
 
 /*Cuando arranca el nodo, se confirma el start, a partir de ahí, se envía Reset
 info para nodo reloj*/
 if (starting == false) {
 	confirmarStart = true;
 } else {
 	confirmarReset = true;
 }
}

/*Funcion que recibe la informacion still_alive del nodo reloj
Si true, el nodo sigue vivo*/

void functionCallback2(const std_msgs::Bool::ConstPtr& msg){
	ROS_INFO("El estado del nodo reloj es: %s", msg ? "true" : "false");
}

//Función principal
int main(int argc, char **argv){
 //registra el nombre del nodo: dialogo_nodo y se crea el handle, denominado nodoDialogo
 ros::init(argc, argv, "dialogo_nodo");
 ros::NodeHandle nodoDialogo;
 ROS_INFO("dialogo_nodo creado y registrado"); //muestra en pantalla

 //si se recibe el mensaje cuyo topic es: "user_topic" se llama a la función manejadora: functionCallback
 ros::Subscriber subscriptorDialogo = nodoDialogo.subscribe("user_topic", 0, functionCallback);
 
 //si se recibe el mensaje cuyo topic es: "still_alive" se llama a la función manejadora: funcionCallback2
 ros::Subscriber subscriptorReloj = nodoDialogo.subscribe("still_alive", 0, functionCallback2);

  //Se invoca el servicio llamado Multiplicador
 client = nodoDialogo.serviceClient<interaccion::multiplicador>("multiplicador");

 //Se publica el mensaje start
 ros::Publisher relojStart = nodoDialogo.advertise<std_msgs::String>("start_topic",0);

  //Se publica el mensaje reset
 ros::Publisher relojReset = nodoDialogo.advertise<std_msgs::String>("reset_topic",0);
 
 while (ros::ok()){
 	 //Cuando el nodo se ejecuta por primera vez, publica el mensaje start
	 if (confirmarStart == true){
	 	std_msgs::String mensajeStart;
	 	std::string start = "start";
	 	mensajeStart.data = start;

	 	relojStart.publish(mensajeStart);

	 	//Una vez publicado, starting = true, indicando que a partir de ahora, se envía reset
	 	confirmarStart = false;
	 	starting = true;
	 }

	 //A partir de que el nodo se ha ejecutado por primera vez, publica el mensaje reset
 	 if (confirmarReset == true){
 		std_msgs::String mensajeReset;
 		std::string reset = "reset";
 		mensajeReset.data = reset;

 		relojReset.publish(mensajeReset);

  		confirmarReset = false;
	 }
	 ros::spinOnce();
	}

 return 0;
}

#include "ros/ros.h"
#include "interaccion/usuario.h"
/**
 * Se implementa un nodo que espera recibir mensajes cuyo topic es "user_topic" del tipo interaccion::usuario.
 * Muestra en pantalla este mensaje recibido
 */
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
}

int main(int argc, char **argv){
 //registra el nombre del nodo: nodo_receptor
 ros::init(argc, argv, "dialogo_nodo");
 ros::NodeHandle nodoDialogo;
 ROS_INFO("dialogo_nodo creado y registrado"); //muestra en pantalla

 //si recibimos el mensaje cuyo topic es: "mensajeTest_topic" llamamos a la función manejadora: funcionCallback
 ros::Subscriber subscriptorDialogo = nodoDialogo.subscribe("user_topic", 0, funcionCallback);

 /** Loop infinito para que no finalice la ejecución del nodo y siempre se pueda llamar al callback */
 ros::spin();
 return 0;
}

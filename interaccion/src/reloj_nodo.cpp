#include "ros/ros.h"
#include "std_msgs/String.h"

/*Se implementa un nodo que se subscriba a los topics start_topic y reset_topic*/


/**
* Esta función muestra por pantalla el mensaje recibido desde el nodo dialogo
*/
void funcionCallback(const std_msgs::String::ConstPtr& msg){
 ROS_INFO("He recibido un mensaje con la informacion: %s", msg->data.c_str());
}

void funcionCallback2(const std_msgs::String::ConstPtr& msg){
 ROS_INFO("He recibido un mensaje con la informacion: %s", msg->data.c_str());
}

int main(int argc, char **argv){
 //registra el nombre del nodo: reloj_nodo
 ros::init(argc, argv, "reloj_nodo");
 ros::NodeHandle nodoReloj;
 ROS_INFO("reloj_nodo creado y registrado"); //muestra en pantalla

 //si recibimos el mensaje cuyo topic es: "start_topic" llamamos a la función manejadora: funcionCallback
 ros::Subscriber subcriptor1 = nodoReloj.subscribe("start_topic", 0, funcionCallback);

  //si recibimos el mensaje cuyo topic es: "reset_topic" llamamos a la función manejadora: funcionCallback2
 ros::Subscriber subscriptor2 = nodoReloj.subscribe("reset_topic", 0, funcionCallback2);


 /** Loop infinito para que no finalice la ejecución del nodo y siempre se pueda llamar al callback */
 ros::spin();
 return 0;
}

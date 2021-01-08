/*Este nodo llamado reloj_nodo muestra la hora UTC, el tiempo transcurrido desde
el ultimo mensaje y envia una señal al dialogo_nodo confirmandole que sigue "vivo"
*/

//Se incluyen las cabeceras
#include "ros/ros.h"
#include "std_msgs/String.h"
#include "std_msgs/Bool.h"
#include <ctime>
#include "boost/date_time/posix_time/posix_time.hpp"

//Declaracion de macros auxiliares
#define RELOJ_MSG_NAME "still_alive"
#define COUNTDOWN_TIME 60


//Declaracion de namespaces
using namespace boost::posix_time;
using namespace ros;
using namespace std;

//Declaracion de variables globales
Time startTime;
bool clock_start = false;
int totalSeconds = 0;

Publisher publicadorTiempo; //Publicador de mensajes que envía still_alive

/**
* Esta función confirma el start recibido desde el nodo_dialogo
*/
void funcionCallback(const std_msgs::String::ConstPtr& msg){
 ROS_INFO("He recibido un mensaje con la informacion: %s", msg->data.c_str());
 startTime = Time::now();
 clock_start = true;
}

//Esta funcion confirma el reset recibido desde el dialogo nodo
void funcionCallback2(const std_msgs::String::ConstPtr& msg){
 ROS_INFO("He recibido un mensaje con la informacion: %s", msg->data.c_str());
 startTime = Time::now();
 clock_start = true;
}

/*timerCallback se ejecuta cada vez que se vence el tiempo del timer
*/
void timerCallback(const ros::TimerEvent&){
	std_msgs::Bool still_alive;
	still_alive.data = true;
	publicadorTiempo.publish(still_alive);
}

/*printClock se encarga de ejecutar la hora UTC
  y de manera adicionar imprime el tiempo transcurrido entre start y reset
*/
void printClock() {
	totalSeconds = (Time::now() - startTime).toSec();	//Segundos desde el inicio hasta el momento actual

	ptime t_local(second_clock::local_time());			//Declaracion de la variable de tiempo local
	ptime t_utc(second_clock::universal_time());		//Declaracion de la variable de tiempo UTC

	ROS_INFO("LOCAL HOUR: %s", to_simple_string(t_local).c_str());
	ROS_INFO("UTC HOUR: %s", to_simple_string(t_utc).c_str());

	ROS_INFO("SECONDS FROM START/RESET: %lf", (double)(Time::now()-startTime).toSec());
}

//funcion principal
int main(int argc, char **argv){
 //registra el nombre del nodo: reloj_nodo
 ros::init(argc, argv, "reloj_nodo");
 ros::NodeHandle nodoReloj;
 ROS_INFO("reloj_nodo creado y registrado"); //muestra en pantalla

 //si recibimos el mensaje cuyo topic es: "start_topic" llamamos a la función manejadora: funcionCallback
 ros::Subscriber subcriptor1 = nodoReloj.subscribe("start_topic", 0, funcionCallback);

  //si recibimos el mensaje cuyo topic es: "reset_topic" llamamos a la función manejadora: funcionCallback2
 ros::Subscriber subscriptor2 = nodoReloj.subscribe("reset_topic", 0, funcionCallback2);
 
 //Timer que se vence cada 60s para indicar que el nodo sigue activo
 Timer timer = nodoReloj.createTimer(Duration(COUNTDOWN_TIME), timerCallback);
 
 //Publicador de mensajes para indicar que el nodo sigue activo
 publicadorTiempo = nodoReloj.advertise<std_msgs::Bool>(RELOJ_MSG_NAME,0);

 //Frecuencia con la que se ejecuta el bucle principal
 ros::Duration seconds_sleep(3);

  while (ros::ok()){
    //Cuando se envie el primer mensaje, se comienza a llamar a printclock
  	if(clock_start){
  		printClock();
    }

    spinOnce();

    ROS_DEBUG("El nodo se duerme durante tres segundos");

    //rate.sleep para cumplir la frecuencia de tres segundos
    seconds_sleep.sleep();
 }
 return 0;
}

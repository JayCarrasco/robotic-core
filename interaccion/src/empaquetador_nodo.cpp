#include "ros/ros.h"
#include "interaccion/inf_personal_usuario.h"
#include "interaccion/usuario.h"
#include "std_msgs/String.h"
#include <string>

using namespace std;

//Estructura para la informacion personal
struct {
    string nombre;
    int edad;
    std::vector<std::string> idiomas;
} infPersonal;

bool confirmacionInfPersonal = false;
bool confirmacionEmocion = false;
/**
 * Se implementa un nodo que espera recibir mensajes cuyo topic es "inf_pers_topic" del tipo interaccion::inf_personal_usuario.
 * Muestra en pantalla este mensaje recibido
 */
/**
* Esta función muestra por pantalla el mensaje recibido que es de tipo inf_personal_usuario
*/

ros::Publisher publicadorEmpaquetador;

//instanciamos un mensaje que queremos enviar
interaccion::usuario mensajeEmpaquetador;

void funcionCallback(const interaccion::inf_personal_usuario::ConstPtr& msg){
 ROS_INFO("He recibido un mensaje de test con el nombre: %s", msg->nombre.c_str());
 ROS_INFO("He recibido un mensaje de test con la edad: %d", msg->edad);
 for (int i = 0; i < msg->idiomas.size(); i++) {
   ROS_INFO("He recibido un mensaje de test con los idiomas: %s", msg->idiomas[i].c_str());
 }

 confirmacionInfPersonal = true;
 ROS_INFO("confirmo info personal: %d", confirmacionInfPersonal);
 mensajeEmpaquetador.infPersonal.edad = msg->edad;
 mensajeEmpaquetador.infPersonal.nombre = msg->nombre;
 mensajeEmpaquetador.infPersonal.idiomas = msg->idiomas;

 //publicadorEmpaquetador.publish(mensajeEmpaquetador);

}

void funcionCallback2(const std_msgs::String::ConstPtr& msg){
 ROS_INFO("He recibido un mensaje con la emocion: %s", msg->data.c_str());

 confirmacionEmocion = true;
 ROS_INFO("confirmo info emocion: %d", confirmacionEmocion);

 mensajeEmpaquetador.emocion = msg->data.c_str();

 //publicadorEmpaquetador.publish(mensajeEmpaquetador);
}

int main(int argc, char **argv){

 //registra el nombre del nodo: empaquetador_nodo
 ros::init(argc, argv, "empaquetador_nodo");

 ros::NodeHandle empaquetadorNodo;

 //Creamos un objeto nodo
 ROS_INFO("empaquetador_nodo creado y registrado"); //muestra en pantalla

 //es necesario "advertir" el tipo de mensaje a enviar y como lo hemos llamado (el topic).
 publicadorEmpaquetador = empaquetadorNodo.advertise<interaccion::usuario>("user_topic",0);

 //si recibimos el mensaje cuyo topic es: "inf_pers_topic" llamamos a la función manejadora: funcionCallback
 ros::Subscriber subscriptor = empaquetadorNodo.subscribe("inf_pers_topic", 0, funcionCallback);

 //si recibimos el mensaje cuyo topic es: "emocion_topic" llamamos a la función manejadora functionCallback2
 ros::Subscriber subscriptor2 = empaquetadorNodo.subscribe("emocion_topic", 0, funcionCallback2);

 while (ros::ok()){
    if (confirmacionEmocion == true and confirmacionInfPersonal == true)
     {
        publicadorEmpaquetador.publish(mensajeEmpaquetador);
        confirmacionEmocion = false;
        confirmacionInfPersonal = false;
    }
    ros::spinOnce();
 }
 // Loop infinito para que no finalice la ejecución del nodo y siempre se pueda llamar al callback


 //tiempo a dormir en cada iteracción
 //ros::Duration seconds_sleep(1);


}

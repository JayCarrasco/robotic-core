//Se incluyen las cabeceras
#include "ros/ros.h"
#include "interaccion/multiplicador.h"

/** Funcion ofertada: multiplicador */
bool multiplicador(interaccion::multiplicador::Request &req, interaccion::multiplicador::Response &res){
 
 //Se multiplica el resultado por 2, y se muestra la peticion y la respuesta
 res.resultado = req.entrada * 2;
 ROS_INFO("Peticion: x = %d", (int)req.entrada);
 ROS_INFO("Respuesta: %d", (int)res.resultado);
 return true;
}

int main(int argc, char **argv){
 //registra el nombre del nodo
 ros::init(argc, argv, "multiplicador_nodo");
 ros::NodeHandle n;

 //registra el servicio
 ros::ServiceServer service = n.advertiseService("multiplicador", multiplicador);
 ROS_INFO("Servicio registrado.");

 //nos quedamos a la espera de llamadas al servicio
 ros::spin();

 return 0;
}
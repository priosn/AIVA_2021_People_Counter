# People Counter
## _Sistema de medición de afluencia_

El objetivo del proyecto consiste en crear una biblioteca de medición de afluencia para un local.
Para ello, se detecta y contabiliza el número de personas que:
1. Recorran el pasillo aledaño al local
2. Permanezcan mirando el escaparate 

La biblioteca recibe una secuencia de video capturada por una cámara exterior al local.

En el proyecto se desarrollará:
- Una biblioteca en Python con las funciones anterior
- Una imagen de Docker para poder ejecutarlo desde cualquier dispositivo.

Este proyecto forma parte de la asignatura de **Aplicaciones Industriales y Comerciales** del [Máster de Visión Artificial](https://breakdance.github.io/breakdance/) de la Universidad Rey Juan Carlos.

## Para ejecutar el proyecto:

### Descargar el código fuente
En primer lugar, para descargar el proyecto se usará el siguiente comando:
```sh
git clone https://github.com/rivers054/AIVA_2021_People_Counter.git
```
### Requisitos del entorno
Se ha ejecutado en un python version 3.8 y se requiere instalar los paquetes paquetes que se encuentran en requirements.txt.
```sh
pip install -r requirements.txt
```
### Ejecución 
Para ejecutar el sistema se introduce como argumento el video que queremos estudiar:
```sh
python PeopleCounter\main.py --input_video [Ruta al video]
```
#### Docker
Adicionalmente se ha creado una imagen Docker con el objetivo de facilitar la ejecución del proyecto. Para ello, únicamente se requiere instalar el programa de Docker y ejecutar los siguientes comandos.
1. Descargar la imagen del repositorio de DockerHub
    ```sh
    docker pull rivers054/peoplecounter:v1
    ```
2. Para crear y ejecutar el contenedor de la imagen descargada. 
    ```sh
    docker run rivers054/peoplecounter:v1
    ```
### Ejecución de test
Se han llevado a cabo test para comprobar correcto funcionamiento del sistema. Para ello, a través de un groundtruth 
tomado por nosotros del video *OneStopNoEnter1front.mpg* es comparado con el resultado del algoritmo implementando en 
biblioteca PeopleCounterLib. Se puede ejecutar con los siguientes comandos:
```
   cd PeopleCounter/
   python PeopleCounterTest.py
```

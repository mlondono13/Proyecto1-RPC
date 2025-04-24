# ST0263-7290

# Estudiantes: Marcela Londoño Leon, mlondonol@eafit.edu.co - Luis Fernando Posada, lfposadac@eafit.edu.co - Juan Martin Betancur, jbetancur5@eafit.edu.co - Jose Miguel Burgos, jmburgoc@eafit.edu.co

# Profesor: Edwin Nelson Montoya Munera, emontoya@eafit.edu.co

# Proyecto 1: Comunicación entre procesos remotos con mecanismo de recuperación de fallas

# 1. Breve descripción
Este proyecto implementa uns sistema de cálculo distribuido utilizando gRPC y RabbitMQ para la comunicación entre procesos remotos. El sistema permite realizar operaciones aritméticas básicas( suma, resta, multiplicación y división) a través de un cliente que se comunica con un servidor mediante un API Gateway. Además, se implementa un mecanismo de recuperación de fallas para garantizar la alta disponibilidad del servicio. 

## 1.1 Aspectos cumplidos

- Implementación de un cliente que se comunica con un API Gateway utilizando gRPC.
- Desarrollo de un API Gateway que enruta las solicitudes a través de RabbitMQ hacia los workers correpondientes
- Creación de workers que realizan operaciones aritméticas básicas y devuelven los resultados al cliente.
- Implementación de un mecanismo de recuperación de fallas para garantizar la disponibilidad del servicio
- Uso de archivos .proto para definir los servicios y mensajes de gRPC
## 1.2 Aspectos no cumplidos
- Implementación de operaciones aritméticas avanzadas (por ejemplo, exponenciación, logaritmos).

# 2. Información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas

La arquitectura del sistema sigue un patrón de microservicios, donde cada componente tiene una responsabilidad específica:​

- Cliente: Interfaz que permite al usuario ingresar operaciones aritméticas y recibir resultados.

- API Gateway: Punto de entrada para las solicitudes del cliente. Se encarga de enrutar las solicitudes a los workers adecuados a través de RabbitMQ.

- RabbitMQ: Sistema de mensajería que facilita la comunicación asincrónica entre el API Gateway y los workers.

- Workers: Procesos que realizan las operaciones aritméticas solicitadas y devuelven los resultados al API Gateway.​

Se utilizaron las siguientes mejores prácticas:​

- Separación de responsabilidades entre los componentes del sistema.

- Uso de gRPC para la comunicación eficiente y escalable entre el cliente y el API Gateway.

- Implementación de un sistema de mensajería (RabbitMQ) para desacoplar los componentes y mejorar la tolerancia a fallos.

- Definición clara de los servicios y mensajes utilizando archivos .proto.

# 3. Descripción del ambiente de desarrollo y técnico: lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.

Lenguaje de programación: Python 3.8

Librerías y paquetes:

grpcio

grpcio-tools

pika

protobuf​


## Detalles del desarrollo
- calculator.proto: Define los servicios y mensajes utilizados en la comunicación gRPC.

- calculator_pb2.py y calculator_pb2_grpc.py: Archivos generados automáticamente a partir de calculator.proto.

- api_gateway.py: Implementa el API Gateway que recibe las solicitudes del cliente y las envía a los workers a través de RabbitMQ.

- rabbitmq_worker.py: Implementa los workers que procesan las operaciones aritméticas.

- calculator_client.py: Implementa el cliente que permite al usuario realizar operaciones aritméticas.​

## Detalles técnicos
El sistema utiliza gRPC para la comunicación entre el cliente y el API Gateway, lo que permite una comunicación eficiente y escalable.

RabbitMQ se utiliza como sistema de mensajería para

opcional - detalles de la organización del código por carpetas o descripción de algún archivo. (ESTRUCTURA DE DIRECTORIOS Y ARCHIVOS IMPORTANTE DEL PROYECTO, comando 'tree' de linux)

opcionalmente - si quiere mostrar resultados o pantallazos

# 4. Descripción del ambiente de EJECUCIÓN (en producción) lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.
IP o nombres de dominio en nube o en la máquina servidor.

## Lenguaje de programación y librerías
El proyecto está desarrollado en Python 3.8 y utiliza las siguientes librerías principales:

Librería	Versión
grpcio	^1.53.0
grpcio-tools	^1.53.0
pika	^1.3.2
protobuf	^4.21.0

## Ambiente de ejecución en producción
El sistema se despliega en la nube utilizando una instancia de AWS Academy:

Proveedor: AWS Academy

Tipo de instancia: t2.micro

Sistema Operativo: Ubuntu Server 20.04 LTS

IP pública (ejemplo): 3.121.45.67 (reemplazar con la real)

Puerto usado por gRPC: 50051

RabbitMQ: Instalado y ejecutándose localmente en la misma máquina

## Configuración de parámetros del sistema
RabbitMQ debe estar instalado y ejecutándose en localhost con el puerto por defecto (5672).

Variables de entorno opcionales:

RABBITMQ_HOST = localhost o IP del broker

RABBITMQ_QUEUE = rpc_queue

Asegúrate de tener los puertos 50051 (gRPC) y 5672 (RabbitMQ) abiertos en el Security Group de la instancia EC2.

## Lanzamiento del sistema en producción

# 1. Conectarse a la instancia EC2
ssh -i "tu-clave.pem" ubuntu@<IP_PUBLICA>

# 2. Clonar el repositorio
git clone https://github.com/mlondono13/Proyecto1-RPC.git
cd Proyecto1-RPC

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Levantar los workers (en una terminal)
python rabbitmq_worker.py

# 5. Levantar el API Gateway (en otra terminal)
python api_gateway.py

# 6. Verificar que RabbitMQ esté corriendo
sudo systemctl status rabbitmq-server


# 5. Información relevante

# Referencias

- awsacademy.instructure.com
- https://pypi.org/project/grpcio/
- https://github.com/st0263eafit/st0263-251/tree/main
- https://pypi.org/project/pika/
- https://pypi.org/project/protobuf/

Este proyecto implementa un middleware para la comunicación asincrónica entre aplicaciones distribuidas, utilizando **RabbitMQ** como sistema de colas de mensajes y **gRPC** como interfaz de comunicación entre cliente y servidor.

---

## Objetivo

Diseñar e implementar un **middleware asincrónico** que permita realizar operaciones matemáticas básicas (**suma, resta, multiplicación y división**) entre aplicaciones distribuidas de forma **eficiente, desacoplada y tolerante a fallos**.

---

## Tecnologías Utilizadas

- Python 3
- gRPC + Protocol Buffers
- RabbitMQ
- Pika (cliente RabbitMQ)
- Protobuf
- Docker (opcional para RabbitMQ)

---

## 🗺Arquitectura General

El sistema se compone de los siguientes módulos:

| Componente             | Descripción                                                                 |
|:----------------------|:----------------------------------------------------------------------------|
| `api_gateway.py`        | Puerta de entrada que expone servicios gRPC y publica los mensajes en RabbitMQ. |
| `calculator.proto`      | Define los servicios y mensajes del sistema usando Protocol Buffers.         |
| `calculator_server.py`  | Servidor gRPC que ofrece operaciones matemáticas básicas.                    |
| `calculator_client.py`  | Cliente gRPC que consume los servicios expuestos por el sistema.              |
| `rabbitmq_worker.py`    | Escucha los mensajes desde RabbitMQ y los distribuye para su procesamiento.  |

---

## Flujo del Sistema

```text
1. El cliente realiza una solicitud a través de gRPC (API Gateway).
2. La API publica el mensaje en una cola RabbitMQ.
3. Un worker escucha esa cola y procesa la operación matemática solicitada.
4. El resultado puede devolverse de forma asincrónica.

## Ejecución del Proyecto

### 1. Instalar dependencias

Asegúrate de tener Python 3 instalado, luego ejecuta:

```bash
pip install -r requirements.txt
```
### 2. Si tienes Docker, puedes levantar RabbitMQ fácilmente con:

```bash
docker run -d --hostname my-rabbit --name rabbitmq \
  -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```
### 3. Abre cuatro terminales y ejecuta en cada una:

```bash
python api_gateway.py
python calculator_server.py
python calculator_client.py
python rabbitmq_worker.py
```
# 4. Una vez todo esté corriendo, prueba el sistema con:

```bah 
python calculator_client.py
```
Esto enviará una solicitud al API Gateway, que será procesada de forma asincrónica y eventualmente devolverá una respuesta desde el worker.

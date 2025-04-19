# Proyecto1-RPC

# 📨 Middleware de Operaciones Matemáticas Asincrónicas entre Aplicaciones

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
| `worker.py`             | Realiza las operaciones matemáticas solicitadas.                             |

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
python calculator_server.py
python rabbitmq_worker.py
python worker.py
python api_gateway.py
```
# 4. Una vez todo esté corriendo, prueba el sistema con:

```bah 
python calculator_client.py
```
Esto enviará una solicitud al API Gateway, que será procesada de forma asincrónica y eventualmente devolverá una respuesta desde el worker.

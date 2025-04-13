# Proyecto1-RPC
# 📨 Middleware de Mensajería Asincrónica entre Aplicaciones

Este proyecto implementa un middleware para la comunicación asincrónica entre aplicaciones distribuidas, utilizando **RabbitMQ** como sistema de colas de mensajes y **gRPC** como interfaz de comunicación entre cliente y servidor.

---

## 📌 Objetivo

Diseñar e implementar un **middleware asincrónico** que permita el envío y procesamiento de mensajes entre aplicaciones distribuidas de forma **eficiente, desacoplada y tolerante a fallos**.

---

## ⚙️ Tecnologías Utilizadas

- Python 3
- gRPC + Protocol Buffers
- RabbitMQ
- Pika (cliente RabbitMQ)
- Protobuf
- Docker (opcional para RabbitMQ)

---

## 🧩 Arquitectura General

El sistema se compone de los siguientes módulos:

| Componente | Descripción |
|------------|-------------|
| `api_gateway.py` | Puerta de entrada que expone servicios gRPC y publica los mensajes en RabbitMQ. |
| `calculator.proto` | Define los servicios y mensajes del sistema usando Protocol Buffers. |
| `calculator_server.py` | Servidor gRPC que ejecuta operaciones de cálculo. |
| `calculator_client.py` | Cliente gRPC que consume los servicios del sistema. |
| `rabbitmq_worker.py` | Escucha los mensajes desde RabbitMQ y los distribuye. |
| `worker.py` | Realiza el procesamiento real de los mensajes recibidos. |

---

## 🔁 Flujo del Sistema

```text
1. El cliente realiza una solicitud a través de gRPC (API Gateway).
2. La API publica el mensaje en una cola RabbitMQ.
3. Un worker escucha esa cola y procesa el mensaje.
4. El resultado puede devolverse de forma asincrónica.

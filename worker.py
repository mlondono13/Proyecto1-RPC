import pika
import json
import grpc
import calculator_pb2
import calculator_pb2_grpc

RABBITMQ_QUEUE = "sum_requests"

def process_request(num1, num2):
    """ Envía la solicitud al servidor gRPC para su procesamiento. """
    try:
        channel = grpc.insecure_channel('localhost:50052')
        stub = calculator_pb2_grpc.CalculatorStub(channel)
        request = calculator_pb2.SumRequest(num1=num1, num2=num2)
        response = stub.Sum(request)
        print(f"✅ Resultado procesado por gRPC: {response.result}")
    except grpc.RpcError:
        print("⚠️ El servidor gRPC sigue inactivo. Mensaje no procesado.")

def callback(ch, method, properties, body):
    """ Procesa los mensajes en la cola de RabbitMQ. """
    message = json.loads(body)
    num1, num2 = message["num1"], message["num2"]
    print(f"📥 Procesando solicitud desde RabbitMQ: {num1} + {num2}")
    process_request(num1, num2)
    ch.basic_ack(delivery_tag=method.delivery_tag)  # Confirma que el mensaje fue recibido

def start_worker():
    """ Inicia el Worker para procesar solicitudes en espera. """
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_QUEUE)
    channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=callback)
    print("📡 Worker escuchando en RabbitMQ... Esperando mensajes.")
    channel.start_consuming()

if __name__ == "__main__":
    start_worker()

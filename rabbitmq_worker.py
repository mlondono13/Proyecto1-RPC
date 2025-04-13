import pika
import grpc
import json
import calculator_pb2
import calculator_pb2_grpc
import time

RABBITMQ_QUEUE = "sum_requests"

def get_grpc_stub():
    channel = grpc.insecure_channel('localhost:60000')
    return calculator_pb2_grpc.CalculatorStub(channel)

def callback(ch, method, properties, body):
    message = json.loads(body)
    num1 = message["num1"]
    num2 = message["num2"]

    try:
        stub = get_grpc_stub()
        request = calculator_pb2.SumRequest(num1=num1, num2=num2)
        response = stub.Sum(request)
        print(f"✅ Procesado desde RabbitMQ: {num1} + {num2} = {response.result}")
        ch.basic_ack(delivery_tag=method.delivery_tag)  # Confirma que se procesó
    except grpc.RpcError as e:
        print("⚠️ No se pudo conectar al servidor gRPC. Reintentando en 5 segundos...")
        time.sleep(5)
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)  # Reintenta después

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_QUEUE)
    channel.basic_qos(prefetch_count=1)  # Procesar un mensaje a la vez
    channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=callback)

    print("🎧 Esperando mensajes en RabbitMQ...")
    channel.start_consuming()

if __name__ == "__main__":
    main()

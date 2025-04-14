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
    operation = message.get("operation", "sum")  # por defecto suma

    try:
        stub = get_grpc_stub()
        request = calculator_pb2.OperationRequest(num1=num1, num2=num2)

        if operation == "sum":
            response = stub.Sum(request)
        elif operation == "sub":
            response = stub.Subtract(request)
        elif operation == "mul":
            response = stub.Multiply(request)
        elif operation == "div":
            response = stub.Divide(request)
        else:
            print(f"❌ Operación '{operation}' no reconocida.")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        print(f"✅ Procesado: {num1} {operation} {num2} = {response.result}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except grpc.RpcError as e:
        print("⚠️ Error de gRPC:", e)
        time.sleep(5)
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

def consume():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_QUEUE)
    channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=callback)
    print("🐰 Esperando mensajes de RabbitMQ. Para salir presiona CTRL+C")
    channel.start_consuming()

if __name__ == "__main__":
    consume()

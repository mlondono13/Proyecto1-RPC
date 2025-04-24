# rabbitmq_worker.py
import pika
import json

def process_message(body):
    data = json.loads(body)
    num1 = data['num1']
    num2 = data['num2']
    operation = data['operation']

    if operation == "sum":
        result = num1 + num2
    elif operation == "sub":
        result = num1 - num2
    elif operation == "mul":
        result = num1 * num2
    elif operation == "div":
        result = num1 / num2 if num2 != 0 else 'Error: División por cero'
    else:
        result = 'Operación no soportada'

    print(f"📬 Mensaje recibido: {data}")
    print(f"✅ Resultado calculado: {result}")

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='sum_requests')

def callback(ch, method, properties, body):
    process_message(body)

print("👂 Esperando mensajes en 'sum_requests'... Ctrl+C para salir")
channel.basic_consume(queue='sum_requests', on_message_callback=callback, auto_ack=True)
channel.start_consuming()

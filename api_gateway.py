from fastapi import FastAPI, HTTPException
import grpc
import calculator_pb2
import calculator_pb2_grpc
import pika
import json

app = FastAPI()
RABBITMQ_QUEUE = "sum_requests"

# Configuración de conexión a RabbitMQ
def send_to_rabbitmq(num1, num2):
    """ Envía la solicitud a RabbitMQ si el servidor gRPC está caído. """
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_QUEUE)

    message = json.dumps({"num1": num1, "num2": num2})
    channel.basic_publish(exchange='', routing_key=RABBITMQ_QUEUE, body=message)
    
    print(f"⚠️ Servidor gRPC no disponible. Enviando mensaje a RabbitMQ: {message}")
    connection.close()

# Conexión con el servidor gRPC
def get_grpc_stub():
    channel = grpc.insecure_channel('localhost:60000')
    return calculator_pb2_grpc.CalculatorStub(channel)

@app.get("/sum/")
def sum_numbers(num1: int, num2: int):
    try:
        stub = get_grpc_stub()
        request = calculator_pb2.SumRequest(num1=num1, num2=num2)
        response = stub.Sum(request)
        return {"result": response.result}
    except grpc.RpcError:
        send_to_rabbitmq(num1, num2)
        raise HTTPException(status_code=503, detail="Servidor gRPC no disponible. La solicitud se ha guardado en RabbitMQ.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

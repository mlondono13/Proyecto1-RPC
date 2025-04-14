from fastapi import FastAPI, HTTPException, Query
import grpc
import calculator_pb2
import calculator_pb2_grpc
import pika
import json

app = FastAPI()
RABBITMQ_QUEUE = "sum_requests"

def send_to_rabbitmq(num1, num2, operation):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_QUEUE)
    message = json.dumps({"num1": num1, "num2": num2, "operation": operation})
    channel.basic_publish(exchange='', routing_key=RABBITMQ_QUEUE, body=message)
    print(f"⚠️ gRPC no disponible. Enviado a RabbitMQ: {message}")
    connection.close()

def get_grpc_stub():
    channel = grpc.insecure_channel('localhost:60000')
    return calculator_pb2_grpc.CalculatorStub(channel)

@app.get("/calculate/")
def calculate(num1: int, num2: int, operation: str = Query("sum", enum=["sum", "sub", "mul", "div"])):
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

        return {"operation": operation, "result": response.result}

    except grpc.RpcError:
        send_to_rabbitmq(num1, num2, operation)
        raise HTTPException(status_code=503, detail="Servidor gRPC no disponible. Solicitud enviada a RabbitMQ.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)

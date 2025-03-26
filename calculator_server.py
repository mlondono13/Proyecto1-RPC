import grpc
from concurrent import futures
import calculator_pb2
import calculator_pb2_grpc

class CalculatorServicer(calculator_pb2_grpc.CalculatorServicer):
    def Sum(self, request, context):
        print(f"Recibido: {request.num1} + {request.num2}")
        result = request.num1 + request.num2
        return calculator_pb2.SumResponse(result=result)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    calculator_pb2_grpc.add_CalculatorServicer_to_server(CalculatorServicer(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    print("Servidor gRPC en ejecución en el puerto 50052")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

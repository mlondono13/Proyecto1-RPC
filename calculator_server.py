from concurrent import futures
import grpc
import calculator_pb2
import calculator_pb2_grpc

class CalculatorServicer(calculator_pb2_grpc.CalculatorServicer):
    def Sum(self, request, context):
        return calculator_pb2.OperationResponse(result=request.num1 + request.num2)

    def Subtract(self, request, context):
        return calculator_pb2.OperationResponse(result=request.num1 - request.num2)

    def Multiply(self, request, context):
        return calculator_pb2.OperationResponse(result=request.num1 * request.num2)

    def Divide(self, request, context):
        if request.num2 == 0:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("División por cero no permitida.")
            return calculator_pb2.OperationResponse()
        return calculator_pb2.OperationResponse(result=request.num1 / request.num2)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    calculator_pb2_grpc.add_CalculatorServicer_to_server(CalculatorServicer(), server)
    server.add_insecure_port('[::]:60000')
    print("🚀 Servidor gRPC corriendo en puerto 60000...")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()

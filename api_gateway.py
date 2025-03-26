from fastapi import FastAPI, HTTPException
import grpc
import calculator_pb2
import calculator_pb2_grpc

app = FastAPI()

def get_grpc_stub():
    channel = grpc.insecure_channel('localhost:50052')
    return calculator_pb2_grpc.CalculatorStub(channel)

@app.get("/sum/")
def sum_numbers(num1: str, num2: str):
    num1, num2 = int(num1), int(num2)
    print(f"📥 Recibido (convertido): num1={num1}, num2={num2}")
    try:
        stub = get_grpc_stub()
        request = calculator_pb2.SumRequest(num1=num1, num2=num2)
        response = stub.Sum(request)
        return {"result": response.result}
    except grpc.RpcError as e:
        raise HTTPException(status_code=500, detail=f"Error en el servidor gRPC: {e.details()}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

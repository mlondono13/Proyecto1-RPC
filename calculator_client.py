import requests

API_GATEWAY_URL = "http://localhost:8001/calculate/"

def run():
    num1 = 30
    num2 = 5
    operation = "sum"  # Cambia entre: sum, sub, mul, div

    response = requests.get(API_GATEWAY_URL, params={
        "num1": num1,
        "num2": num2,
        "operation": operation
    })

    if response.status_code == 200:
        data = response.json()
        print(f"✅ {operation.upper()} Resultado: {data['result']}")
    else:
        print(f"⚠️ Error en el API Gateway: {response.status_code} - {response.text}")

if __name__ == "__main__":
    run()

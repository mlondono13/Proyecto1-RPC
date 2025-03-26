import requests

API_GATEWAY_URL = "http://localhost:8000/sum/"

def run():
    num1 = 30
    num2 = 30
    response = requests.get(API_GATEWAY_URL, params={"num1": num1, "num2": num2})

    if response.status_code == 200:
        data = response.json()
        print(f"✅ Respuesta del API Gateway: {data['result']}")
    else:
        print(f"⚠️ Error en el API Gateway: {response.status_code} - {response.text}")

if __name__ == "__main__":
    run()

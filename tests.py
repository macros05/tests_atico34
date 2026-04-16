import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_match_cliente():
    print("\n--- TEST: POST /match ---")
    payload = {
        "nombre": "Empresa Test RGPD",
        "descripcion": "Empresa mediana que necesita cumplir con el RGPD urgentemente"
    }
    response = requests.post(f"{BASE_URL}/match", json=payload)
    data = response.json()
    print(f"Status: {response.status_code}")
    print(f"Respuesta: {json.dumps(data, indent=2, ensure_ascii=False)}")
    assert response.status_code == 200
    assert "cliente_id" in data
    assert "comercial_asignado" in data
    print("TEST PASADO")
    return data["cliente_id"]

def test_historial():
    print("\n--- TEST: GET /historial_clientes ---")
    response = requests.get(f"{BASE_URL}/historial_clientes")
    data = response.json()
    print(f"Status: {response.status_code}")
    print(f"Total registros: {len(data)}")
    assert response.status_code == 200
    print("TEST PASADO")

def test_clientes_no_revisados():
    print("\n--- TEST: GET /clientes_no_revisados ---")
    response = requests.get(f"{BASE_URL}/clientes_no_revisados")
    data = response.json()
    print(f"Status: {response.status_code}")
    print(f"Pendientes de revisión: {len(data)}")
    assert response.status_code == 200
    print("TEST PASADO")

def test_revisar_cliente(cliente_id):
    print(f"\n--- TEST: POST /revisar_cliente/{cliente_id} ---")
    response = requests.post(f"{BASE_URL}/revisar_cliente/{cliente_id}")
    data = response.json()
    print(f"Status: {response.status_code}")
    print(f"Respuesta: {json.dumps(data, indent=2, ensure_ascii=False)}")
    assert response.status_code == 200
    assert "message" in data
    print("TEST PASADO")

if __name__ == "__main__":
    print("INICIANDO TESTS DEL SISTEMA DE MATCHING")
    print("=" * 50)
    
    cliente_id = test_match_cliente()
    test_historial()
    test_clientes_no_revisados()
    test_revisar_cliente(cliente_id)
    
    print("\n" + "=" * 50)
    print("TODOS LOS TESTS PASADOS")
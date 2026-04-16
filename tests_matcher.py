import requests
import pandas as pd
import json

# --- CONFIGURACIÓN ---
BASE_URL = "http://127.0.0.1:8000" 
MATCH_ENDPOINT = f"{BASE_URL}/match"
CSV_FILE_PATH = "clientes_a_probar.csv" #

def load_test_cases(file_path):
    """Carga los casos de prueba desde el CSV."""
    try:
        df = pd.read_csv(file_path)
        print(f"✅ Datos cargados exitosamente desde {file_path}. Total de clientes a probar: {len(df)}")
        
        test_cases = []
        for index, row in df.iterrows():
            test_cases.append({
                "nombre": str(row['nombre']), 
                "descripcion": str(row['descripcion'])
            })
        return test_cases
    except FileNotFoundError:
        print(f"\n❌ ERROR FATAL: No se encontró el archivo '{file_path}'. Por favor, créalo.")
        return []

def test_matcher(test_cases):
    """Itera sobre los casos de prueba y llama al endpoint /match."""
    if not test_cases:
        print("No hay casos de prueba para ejecutar. Terminando el script.")
        return

    print("\n=========================================================")
    print("🚀 INICIANDO PRUEBAS AUTOMATIZADAS DEL MOTOR DE MATCHING 🤖")
    print("=========================================================\n")

    for i, caso in enumerate(test_cases):
        print(f"--- [PRUEBA {i+1}/{len(test_cases)}] ---")
        print(f"Cliente a probar: {caso['nombre']}")
        # Mostramos solo un fragmento de la descripción para no saturar la consola
        print(f"Descripción enviada: '{caso['descripcion'][:60]}...'")

        # 1. Preparar el payload (el cuerpo de la solicitud)
        payload = {
            "nombre": caso["nombre"],
            "descripcion": caso["descripcion"]
        }
        
        try:
            # 2. Realizar la llamada POST al endpoint de FastAPI
            response = requests.post(MATCH_ENDPOINT, json=payload)
            
            # 3. Procesar la respuesta
            if response.status_code == 200:
                result = response.json()
                asignado = result.get("comercial_asignado", "NO ENCONTRADO")
                print(f"✅ ÉXITO de conexión.")
                print(f"   -> Resultado recibido: {asignado}")
            else:
                print(f"❌ FALLO en la llamada a la API. Código HTTP: {response.status_code}")
                print(f"   -> Respuesta del servidor: {response.text}")

        except requests.exceptions.ConnectionError:
            print("\n=========================================================")
            print("🚨 ERROR FATAL DE CONEXIÓN 🚨")
            print("Asegúrate de que tu aplicación FastAPI esté corriendo en la URL correcta:")
            print(f"   -> {BASE_URL}")
            break # Detener el bucle si no hay conexión

if __name__ == "__main__":
    # Cargar los casos de prueba primero
    test_cases = load_test_cases(CSV_FILE_PATH)
    
    # Ejecutar las pruebas
    test_matcher(test_cases)

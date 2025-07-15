import requests
import os
import zipfile
import io

def descargar_crd(semana):
    """
    Descarga y extrae el archivo .CRD de la semana especificada (desde la API del IGAC).
    
    Args:
        semana (int or str): Semana GPS en formato numérico o string (e.g., 2357 o "2357")
    """
    semana_str = str(semana)  # Asegura que sea string
    nombre_archivo = f"IGA{semana_str}.CRD"
    carpeta_semana = os.path.join("descargas", semana_str)
    os.makedirs(carpeta_semana, exist_ok=True)

    payload = {
        "datos": [f"./CoordenadasSemanales/{nombre_archivo}"]
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0",
        "Accept": "*/*",
        "Content-Type": "application/json",
        "Referer": "https://redgeodesica.igac.gov.co/",
    }

    url = "https://ccg.igac.gov.co/api/rinex"
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200 and response.content:
        try:
            with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
                zip_ref.extractall(carpeta_semana)
                print(f"✅ Archivo {nombre_archivo} extraído en: {carpeta_semana}")
        except zipfile.BadZipFile:
            print(f"⚠️ El archivo recibido no es un ZIP válido para la semana {semana_str}")
    else:
        print(f"❌ Error al descargar {nombre_archivo} - Status: {response.status_code}")

# Puedes usar strings o números, ambos funcionarán
"""
semanas = [2327, "2328", 2357]

for semana in semanas:
    descargar_crd(semana)

"""

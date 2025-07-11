import os
import re
from bs4 import BeautifulSoup
import pandas as pd

def extraer_datos_html(path):
    with open(path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    # Fecha de inicio
    texto_fechas = soup.find("h2", string=re.compile("Par[áa]metros de Procesamiento.*"))
    fecha_inicio = (
        re.search(r"(\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2})", texto_fechas.text).group(1)
        if texto_fechas else None
    )

    # Nombre del móvil
    nombre_movil_match = soup.find("h1", string=re.compile("L[ií]nea base.*-.*"))
    nombre_movil = (
        nombre_movil_match.text.split("-")[-1].strip() if nombre_movil_match else None
    )

    # Coordenadas cartesianas del móvil (X, Y, Z)
    x, y, z = None, None, None
    tablas = soup.find_all("table", class_="summary")
    for tabla in tablas:
        filas = tabla.find_all("tr")
        for fila in filas:
            celdas = fila.find_all("td")
            if len(celdas) >= 3:
                etiqueta = celdas[0].text.strip()
                valor = celdas[2].text.strip().lower().replace("m", "").strip()
                valor = valor.replace(".", "").replace(",", ".")
                try:
                    if "Cartesiana X" in etiqueta:
                        x = float(valor)
                    elif "Cartesiana Y" in etiqueta:
                        y = float(valor)
                    elif "Cartesiana Z" in etiqueta:
                        z = float(valor)
                except ValueError:
                    pass

    return {
        "archivo": os.path.basename(path),
        "fecha_inicio": fecha_inicio,
        "nombre_movil": nombre_movil,
        "x": x,
        "y": y,
        "z": z,
    }

# Ruta donde están los archivos HTML
carpeta = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "descargas", "reportes")
)

datos = []
for archivo in os.listdir(carpeta):
    if archivo.endswith(".html"):
        ruta = os.path.join(carpeta, archivo)
        datos.append(extraer_datos_html(ruta))

# Crear DataFrame
df = pd.DataFrame(datos)

# Convertir a datetime
df['fecha_inicio'] = pd.to_datetime(df['fecha_inicio'], format='%d/%m/%Y %H:%M:%S')

# Ordenar por fecha
df = df.sort_values(by='fecha_inicio')
print(df)

# exportar datos a xlsx
df.to_excel("coordenadas_extraidas.xlsx", index=False, engine='openpyxl')
df.to_csv("coordenadas_extraidas.csv", index=False)

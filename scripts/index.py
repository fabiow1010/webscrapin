import os
from script import descargar_GPS, descargar_glonass
from semanas import descargar_crd_semanas  
from semanas2 import descargar_crd
from analisis import analizar_estaciones
from extracion import extraer_coordenadas_desde_htmls
from deslpazamientos import generar_graficas_desplazamientos

# Parámetros
semanas = [2335,2336,2337,2338]
estaciones = ["BOGA", "BOGT"]
dia_central = 6
ruta_excel = "coordenadas_extraidas.xlsx"
carpeta_salidas = "graficas_salida"

# 1. Descarga GPS y GLONASS
try:
    print("✅ Descarga de archivos GPS y GLONASS iniciada.")
    descargar_GPS(semanas, dia_central)
    descargar_glonass(semanas, dia_central)
    print("✅ Descarga de archivos GPS y GLONASS completada.")
except Exception as e:
    print(f"❌ Error al descargar GPS/GLONASS: {e}")

# 2. Descarga CRD de SIRGAS
try:
    descargar_crd_semanas(semanas)
    print("✅ Descarga de archivos CRD de SIRGAS completada.")
except Exception as e:
    print(f"❌ Error al descargar CRD de SIRGAS: {e}")

# 3. Descarga CRD de IGAC
for semana in semanas:
    try:
        descargar_crd(semana)
        print(f"✅ Descarga de CRD IGAC para semana {semana} completada.")
    except Exception as e:
        print(f"❌ Error al descargar CRD de IGAC para semana {semana}: {e}")

# 4. Análisis de estaciones base
## se deden tener almenos tres semanas analizadas para un análisis significativo.
try:
    analizar_estaciones(semanas, estaciones)
    print("✅ Análisis de estaciones completado.")
except Exception as e:
    print(f"❌ Error en análisis de estaciones: {e}")

# 5. Extracción de coordenadas desde HTMLs
try:
    print("✅ Extracción de coordenadas desde HTMLs iniciada.")
    carpeta = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "descargas", "reportes"))
    df = extraer_coordenadas_desde_htmls(carpeta)
    print("✅ Extracción de coordenadas desde HTMLs completada.")
except Exception as e:
    print(f"❌ Error extrayendo coordenadas desde HTMLs: {e}")

# 6. Generación de gráficas de desplazamientos
try:
    print("✅ Generación de gráficas de desplazamientos iniciada.")
    generar_graficas_desplazamientos(ruta_excel, carpeta_salidas)
    print("✅ Generación de gráficas de desplazamientos completada.")
except Exception as e:
    print(f"❌ Error al generar gráficas de desplazamientos: {e}")

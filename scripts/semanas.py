from ftplib import FTP
import pandas as pd 
import os
import numpy as np
import matplotlib.pyplot as plt

## conexion al servidor ftp

# Conexión anónima a SIRGAS
try:
    ftp = FTP('ftp.sirgas.org')
    ftp.login()
    print("Conectado a SIRGAS.")
except Exception as e:
    print(f"Error al conectar a SIRGAS: {e}")
""""
# Conexión autenticada a IGAC
try:
    pass
    ftp = FTP('132.255.20.140')
    ftp.login()
    print("Conexión exitosa al servidor FTP de IGAC.")
except Exception as e:
    print(f"Error al conectar al servidor FTP de IGAC: {e}")
"""
"""

semanas = [
    "1982", "1986", "1990", "1995", "1999", "2003", "2008", "2012", "2016", "2021", "2025", "2029", "2034", "2038", "2042", "2047",
    "2051", "2055", "2060", "2064", "2069", "2073", "2077", "2082", "2086", "2090", "2095", "2099", "2103", "2108", "2112", "2116",
    "2121", "2125", "2130", "2134", "2138", "2143", "2147", "2151", "2155", "2160", "2164", "2169", "2173", "2177", "2182", "2186",
    "2190", "2195", "2199", "2203", "2208", "2212", "2216", "2221", "2225", "2229", "2234", "2238", "2243", "2247", "2251", "2255",
    "2260", "2264", "2268", "2273", "2277", "2282", "2286", "2290", "2295", "2299", "2303", "2308", "2312", "2316", "2321", "2325",
    "2330", "2334", "2338", "2343"
]

"""

semanas = ["2327", "2328","2329","2330","2331","2335","2336","2336"]

print("Semanas a descargar:", len(semanas))


## descargar archivos CRD


# Ruta a la carpeta de salidas dentro de 'salidas'
ruta_base_descargas = os.path.abspath("descargas")
os.makedirs(ruta_base_descargas, exist_ok=True)


print("📂 Listando semanas disponibles en SIRGAS...")
for semana in semanas:
    print(f"\n📂 Procesando semana {semana}...")

    try:
        ftp.cwd(f'/pub/gps/SIRGAS/{semana}/')

        archivos = ftp.nlst()
        archivo_crd = next((a for a in archivos if semana in a and a.endswith('.crd')), None)

        if archivo_crd:
            print(f"📥 Descargando archivo: {archivo_crd}")
            carpeta_semana = os.path.join(ruta_base_descargas, semana)
            os.makedirs(carpeta_semana, exist_ok=True)

            ruta_archivo = os.path.join(carpeta_semana, archivo_crd)
            with open(ruta_archivo, 'wb') as f:
                ftp.retrbinary(f'RETR {archivo_crd}', f.write)
        else:
            print(f"❌ No se encontró archivo .crd para la semana {semana}")

        ftp.cwd('/')

    except Exception as e:
        print(f"❌ No se pudo acceder a la semana {semana}: {e}")
        continue

# Cerrar la conexión después del bucle
ftp.quit()
print("\n✅ Descarga finalizada.")


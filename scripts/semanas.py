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

semanas = ["1185", "1186"]

print("Semanas a descargar:", len(semanas))


## descargar archivos CRD


# Ruta a la carpeta de salidas dentro de 'salidas'
ruta_salida_base = os.path.abspath("salidas")
os.makedirs(ruta_salida_base, exist_ok=True)

print("📂 Listando semanas disponibles en SIRGAS...")
for semana in semanas:
    print(f"\n📂 Procesando semana {semana}...")
    
    try:
        ftp.cwd(f'/pub/gps/SIRGAS/{semana}/')  # Cambiar al directorio de la semana
        
        # Obtener lista de archivos
        archivos = ftp.nlst()

        # Buscar archivo .crd que contenga el número de semana
        archivo_crd = next((a for a in archivos if semana in a and a.endswith('.crd')), None)

        if archivo_crd:
            print(f"📥 Descargando archivo: {archivo_crd}")
            ruta_archivo = os.path.join(ruta_salida_base, archivo_crd)
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

## analisis de cada archivo crd
folder = os.path.abspath("salidas")
print(f"📁 Accediendo a carpeta: {folder}")

# Verifica si existe y muestra contenido
if os.path.exists(folder):
    archivos = os.listdir(folder)
    print(f"📄 Archivos encontrados: {archivos}")
else:
    print("❌ La carpeta no existe")
# Lista para guardar los DataFrames filtrados de cada archivo
dfs = []

# Columnas y tipos para leer los archivos .crd
columnas= ['NUM', 'STATION', 'NAME', 'X (M)', 'Y (M)','Z (M)', 'FLAG']
tipos = {
    'NUM': str,
    'STATION':str,
    'NAME': str,
    'X (M)': float,
    'Y (M)': float,
    'Z (M)': float,
    'FLAG': str
}

# Iterar por cada archivo en la carpeta 'salidas'
for archivo in os.listdir(folder):
    if archivo.endswith('.crd'):
        ruta = os.path.join(folder, archivo)
        # Leer el archivo .crd
        # Extraer la semana del nombre del archivo (asumiendo que contiene el número de semana como '20XX')
        semana = ''.join(filter(str.isdigit, archivo))[:4]  # Ajusta si el formato de nombre cambia

        # Leer el archivo .crd
        df = pd.read_csv(ruta, sep=r'\s+', skiprows=6, names=columnas, dtype=tipos)

        # Filtrar por STATION == 'BOGA'
        df = df[df['STATION'] == 'BOGA']

        # Añadir la columna de semana si hay datos
        if not df.empty:
            df['SEMANA'] = semana  # Añade columna SEMANA como str
            dfs.append(df)

# Concatenar todos los DataFrames filtrados
if dfs:
    DATA = pd.concat(dfs, ignore_index=True)
    # Exportar el resultado a un CSV en 'data/'
    output_csv = os.path.abspath(os.path.join("salidas", "DATA.csv"))
    DATA.to_csv(output_csv, index=False)

else:
    DATA = pd.DataFrame(columns=columnas)  # 

print(DATA.info())
print(DATA.describe())
print(DATA)


## plotear los datos

DATA[['X (M)', 'Y (M)', 'Z (M)']] = DATA[['X (M)', 'Y (M)', 'Z (M)']].apply(pd.to_numeric)

# Estadísticas básicas
summary = DATA[['X (M)', 'Y (M)', 'Z (M)']].describe()
print("📊 Estadísticas resumidas:")
print(summary)
# Cambios absolutos respecto al primer valor
ref = DATA.iloc[0][['X (M)', 'Y (M)', 'Z (M)']]
DATA['delta_X'] = DATA['X (M)'] - ref['X (M)']
DATA['delta_Y'] = DATA['Y (M)'] - ref['Y (M)']
DATA['delta_Z'] = DATA['Z (M)'] - ref['Z (M)']
print("\n📈 Cambios máximos respecto al primer punto:")
# Gráficos de cambio en X, Y y Z respecto al primer valor

# Gráficos de cambio en X, Y y Z respecto al primer valor (comparando respecto al primer dato)
#define los parametros de las figuras
fig, axs = plt.subplots(3, 1, figsize=(12, 12), sharex=True)
#declara los titulos de las figuras
fig.suptitle('Cambios en coordenadas X, Y, Z respecto al primer dato', fontsize=16)

#declara valores para los ejes de X[M]
axs[0].plot(DATA.index, DATA['delta_X'], marker='o', label='ΔX respecto al primer dato')
axs[0].axhline(0, color='gray', linestyle='--')
axs[0].set_ylabel('ΔX (m)')
axs[0].set_title('Cambio en X respecto al primer dato')
axs[0].legend()
axs[0].grid(True)
#declara valores para los ejes de Y[M]
axs[1].plot(DATA.index, DATA['delta_Y'], marker='o', color='orange', label='ΔY respecto al primer dato')
axs[1].axhline(0, color='gray', linestyle='--')
axs[1].set_ylabel('ΔY (m)')
axs[1].set_title('Cambio en Y respecto al primer dato')
axs[1].legend()
axs[1].grid(True)

#declara valores para los ejes de Z[M]
axs[2].plot(DATA.index, DATA['delta_Z'], marker='o', color='green', label='ΔZ respecto al primer dato')
axs[2].axhline(0, color='gray', linestyle='--')
axs[2].set_ylabel('ΔZ (m)')
axs[2].set_title('Cambio en Z respecto al primer dato')
axs[2].legend()
axs[2].grid(True)

plt.xlabel('Observación')
plt.tight_layout()
plt.show()
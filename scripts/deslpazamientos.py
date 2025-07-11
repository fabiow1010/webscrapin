import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Leer el archivo Excel
ruta_excel = "coordenadas_extraidas.xlsx"
df = pd.read_excel(ruta_excel, engine='openpyxl')
df['fecha_inicio'] = pd.to_datetime(df['fecha_inicio'])

# Calcular deltas
df = df.sort_values(['punto', 'fecha_inicio']).reset_index(drop=True)
deltas = df.groupby('punto')[['x', 'y', 'z']].diff().rename(columns=lambda col: f'delta_{col}')
df = pd.concat([df, deltas], axis=1)

# Carpeta de salida
output_dir = "graficas_salida"
os.makedirs(output_dir, exist_ok=True)

# Función para generar y guardar gráficas individuales
def graficar_y_guardar(df, eje):
    for punto, grupo in df.groupby('punto'):
        fechas = grupo['fecha_inicio']
        deltas = grupo[f'delta_{eje}']

        plt.figure(figsize=(10, 6))
        plt.plot(fechas, deltas, marker='o', label=punto)
        
        # Línea de tendencia
        datos_validos = deltas.notna()
        if datos_validos.sum() > 1:
            x_ord = fechas[datos_validos].map(pd.Timestamp.toordinal)
            y_vals = deltas[datos_validos]
            coef = np.polyfit(x_ord, y_vals, 1)
            tendencia = np.poly1d(coef)(x_ord)
            plt.plot(fechas[datos_validos], tendencia, linestyle='--', label='Tendencia')

        plt.title(f'Δ{eje.upper()} a lo largo del tiempo - Punto: {punto}')
        plt.xlabel('Fecha')
        plt.ylabel(f'Cambio en {eje.upper()}')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()

        # Guardar gráfico
        nombre_archivo = f"{punto}_delta_{eje}.png".replace(" ", "_").replace("/", "_")
        ruta_salida = os.path.join(output_dir, nombre_archivo)
        plt.savefig(ruta_salida)
        plt.close()

# Generar y guardar gráficas por eje y punto
for eje in ['x', 'y', 'z']:
    graficar_y_guardar(df, eje)

print(f"✅ Todas las gráficas han sido guardadas en la carpeta '{output_dir}'")

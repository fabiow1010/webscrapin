import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def generar_graficas_desplazamientos(ruta_excel, output_dir="graficas_salida"):
    df = pd.read_excel(ruta_excel, engine='openpyxl')
    df['fecha_inicio'] = pd.to_datetime(df['fecha_inicio'])

    df = df.sort_values(['ZONA REAL', 'fecha_inicio']).reset_index(drop=True)
    deltas = df.groupby('ZONA REAL')[['x', 'y', 'z']].diff().rename(columns=lambda col: f'delta_{col}')
    df = pd.concat([df, deltas], axis=1)

    os.makedirs(output_dir, exist_ok=True)

    def graficar_y_guardar(df, eje):
        for punto, grupo in df.groupby('ZONA REAL'):
            fechas = grupo['fecha_inicio']
            deltas = grupo[f'delta_{eje}']

            plt.figure(figsize=(10, 6))
            plt.plot(fechas, deltas, marker='o', label=punto)
            
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

            nombre_archivo = f"{punto}_delta_{eje}.png".replace(" ", "_").replace("/", "_")
            ruta_salida = os.path.join(output_dir, nombre_archivo)
            plt.savefig(ruta_salida)
            plt.close()

    for eje in ['x', 'y', 'z']:
        graficar_y_guardar(df, eje)

    print(f"✅ Todas las gráficas han sido guardadas en la carpeta '{output_dir}'")

# Ejemplo de uso desde otro archivo:
# from deslpazamientos import generar_graficas_desplazamientos
# generar_graficas_desplazamientos("coordenadas_extraidas.xlsx", "graficas_salida")

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


def analizar_estaciones(semanas, estaciones_a_buscar, ruta_base_descargas="descargas"):
    # Convertir todas las semanas a string
    semanas = [str(s) for s in semanas]

    # Ruta base
    ruta_base_descargas = os.path.abspath(ruta_base_descargas)
    os.makedirs(ruta_base_descargas, exist_ok=True)

    # Columnas y tipos esperados
    columnas = ["NUM", "STATION", "NAME", "X (M)", "Y (M)", "Z (M)", "FLAG"]
    tipos = {
        "NUM": str,
        "STATION": str,
        "NAME": str,
        "X (M)": float,
        "Y (M)": float,
        "Z (M)": float,
        "FLAG": str,
    }

    def leer_estaciones_crd(semanas, estaciones):
        dfs = []
        for semana in semanas:
            carpeta_semana = os.path.join(ruta_base_descargas, semana)
            if os.path.exists(carpeta_semana):
                for archivo in os.listdir(carpeta_semana):
                    if archivo.lower().endswith(".crd"):
                        ruta = os.path.join(carpeta_semana, archivo)
                        try:
                            df = pd.read_csv(
                                ruta,
                                sep=r"\s+",
                                skiprows=6,
                                names=columnas,
                                dtype=tipos,
                            )
                            df_filtrado = df[df["STATION"].isin(estaciones)]
                            if not df_filtrado.empty:
                                df_filtrado["SEMANA"] = semana
                                dfs.append(df_filtrado)
                        except Exception as e:
                            print(f"⚠️ Error leyendo {ruta}: {e}")
        if dfs:
            return pd.concat(dfs, ignore_index=True)
        else:
            return pd.DataFrame(columns=columnas)

    # Leer datos
    DATA = leer_estaciones_crd(semanas, estaciones_a_buscar)

    # Guardar CSV si hay datos
    if not DATA.empty:
        output_csv = os.path.join(ruta_base_descargas, "DATA.csv")
        DATA.to_csv(output_csv, index=False)

    # Análisis
    print(DATA.info())
    print(DATA.describe())
    print(DATA)

    # Asegura tipo numérico
    DATA[["X (M)", "Y (M)", "Z (M)"]] = DATA[["X (M)", "Y (M)", "Z (M)"]].apply(
        pd.to_numeric
    )

    # Estadísticas generales
    print("📊 Estadísticas resumidas generales:")
    print(DATA[["X (M)", "Y (M)", "Z (M)"]].describe())

    # Carpeta para guardar gráficos
    carpeta_graficas = os.path.join(ruta_base_descargas, "graficas_estaciones")
    os.makedirs(carpeta_graficas, exist_ok=True)

    # ... (todo el código anterior igual hasta:)

    # Agrupar por estación
    for estacion, grupo in DATA.groupby("STATION"):
        print(f"\n📍 Procesando estación: {estacion}")

        # Ordenar por semana
        grupo = grupo.sort_values(by="SEMANA")

        # Referencia: primer valor de coordenadas
        ref = grupo.iloc[0][["X (M)", "Y (M)", "Z (M)"]]
        grupo["delta_X"] = grupo["X (M)"] - ref["X (M)"]
        grupo["delta_Y"] = grupo["Y (M)"] - ref["Y (M)"]
        grupo["delta_Z"] = grupo["Z (M)"] - ref["Z (M)"]

        # Validar que hay al menos 2 observaciones y que no hay NaN
        if (
            len(grupo) < 2
            or grupo[["delta_X", "delta_Y", "delta_Z"]].isnull().any().any()
        ):
            print(
                f"⚠️ No se puede calcular la tendencia para estación {estacion} (datos insuficientes o valores nulos)"
            )
            continue  # Saltar esta estación

        # Estadísticas resumidas por estación
        print(grupo[["delta_X", "delta_Y", "delta_Z"]].describe())

        # Crear índice relativo para las gráficas
        x_vals = np.arange(len(grupo))

        # Gráficos por estación
        fig, axs = plt.subplots(3, 1, figsize=(12, 12), sharex=True)
        fig.suptitle(
            f"Cambios en coordenadas X, Y, Z - Estación {estacion}", fontsize=16
        )

        # ΔX
        axs[0].plot(x_vals, grupo["delta_X"], marker="o", label="ΔX")
        coef_x = np.polyfit(x_vals, grupo["delta_X"], 1)
        trend_x = np.poly1d(coef_x)
        axs[0].plot(
            x_vals, trend_x(x_vals), color="red", linestyle="--", label="Tendencia ΔX"
        )
        axs[0].axhline(0, color="gray", linestyle="--")
        axs[0].set_ylabel("ΔX (m)")
        axs[0].set_title("Cambio en X")
        axs[0].legend()
        axs[0].grid(True)

        # ΔY
        axs[1].plot(x_vals, grupo["delta_Y"], marker="o", color="orange", label="ΔY")
        coef_y = np.polyfit(x_vals, grupo["delta_Y"], 1)
        trend_y = np.poly1d(coef_y)
        axs[1].plot(
            x_vals, trend_y(x_vals), color="red", linestyle="--", label="Tendencia ΔY"
        )
        axs[1].axhline(0, color="gray", linestyle="--")
        axs[1].set_ylabel("ΔY (m)")
        axs[1].set_title("Cambio en Y")
        axs[1].legend()
        axs[1].grid(True)

        # ΔZ
        axs[2].plot(x_vals, grupo["delta_Z"], marker="o", color="green", label="ΔZ")
        coef_z = np.polyfit(x_vals, grupo["delta_Z"], 1)
        trend_z = np.poly1d(coef_z)
        axs[2].plot(
            x_vals, trend_z(x_vals), color="red", linestyle="--", label="Tendencia ΔZ"
        )
        axs[2].axhline(0, color="gray", linestyle="--")
        axs[2].set_ylabel("ΔZ (m)")
        axs[2].set_title("Cambio en Z")
        axs[2].legend()
        axs[2].grid(True)

        plt.xlabel("Observación")
        plt.tight_layout()

        # Guardar gráfico
        nombre_archivo = f"{estacion}_desplazamientos.png".replace(" ", "_")
        ruta_grafica = os.path.join(carpeta_graficas, nombre_archivo)
        plt.savefig(ruta_grafica)
        plt.close()
        print(f"✅ Gráfica guardada: {ruta_grafica}")

    return DATA  # <-- Esto es necesario para retornar el DataFrame resultante


# Ejemplo de uso:

"""
semanas = [2327, "2328", 2357]  # Enteros o cadenas
estaciones = ["BOGA", "BOGT"]
analizar_estaciones(semanas, estaciones)
"""

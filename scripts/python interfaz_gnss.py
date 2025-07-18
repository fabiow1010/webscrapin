import tkinter as tk
from tkinter import filedialog, messagebox
from script import descargar_GPS, descargar_glonass
from semanas import descargar_crd_semanas  
from semanas2 import descargar_crd
from analisis import analizar_estaciones
from extracion import extraer_coordenadas_desde_htmls
from deslpazamientos import generar_graficas_desplazamientos
import os

# Funciones asociadas a los botones
def ejecutar_descarga_gps_glonass():
    try:
        semanas = [int(s) for s in entry_semanas.get().split(',')]
        dia_central = int(entry_dia.get())
        descargar_GPS(semanas, dia_central)
        descargar_glonass(semanas, dia_central)
        messagebox.showinfo("Éxito", "GPS y GLONASS descargados correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al descargar GPS/GLONASS:\n{e}")

def ejecutar_descarga_crd_sirgas():
    try:
        semanas = [int(s) for s in entry_semanas.get().split(',')]
        descargar_crd_semanas(semanas)
        messagebox.showinfo("Éxito", "CRD SIRGAS descargados correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al descargar CRD SIRGAS:\n{e}")

def ejecutar_descarga_crd_igac():
    semanas = [int(s) for s in entry_semanas.get().split(',')]
    errores = []
    for semana in semanas:
        try:
            descargar_crd(semana)
        except Exception as e:
            errores.append(f"Semana {semana}: {e}")
    if errores:
        messagebox.showwarning("Finalizado con errores", "\n".join(errores))
    else:
        messagebox.showinfo("Éxito", "CRD IGAC descargados correctamente.")

def ejecutar_analisis_estaciones():
    try:
        semanas = [int(s) for s in entry_semanas.get().split(',')]
        estaciones = [e.strip().upper() for e in entry_estaciones.get().split(',')]
        analizar_estaciones(semanas, estaciones)
        messagebox.showinfo("Éxito", "Análisis de estaciones completado.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al analizar estaciones:\n{e}")

def ejecutar_extraccion_coordenadas():
    try:
        carpeta = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "descargas", "reportes"))
        extraer_coordenadas_desde_htmls(carpeta)
        messagebox.showinfo("Éxito", "Extracción de coordenadas completada.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al extraer coordenadas:\n{e}")

def ejecutar_graficas_desplazamiento():
    try:
        ruta_excel = entry_excel.get()
        carpeta_salidas = entry_salida.get()
        generar_graficas_desplazamientos(ruta_excel, carpeta_salidas)
        messagebox.showinfo("Éxito", "Gráficas generadas correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Error al generar gráficas:\n{e}")

# --- Interfaz gráfica ---
root = tk.Tk()
root.title("GNSS Pipeline - IGAC / SIRGAS")
root.geometry("600x500")

# --- Entradas ---
tk.Label(root, text="Semanas (separadas por coma)").pack()
entry_semanas = tk.Entry(root, width=50)
entry_semanas.insert(0, "2335,2336,2337,2338")
entry_semanas.pack()

tk.Label(root, text="Estaciones (separadas por coma)").pack()
entry_estaciones = tk.Entry(root, width=50)
entry_estaciones.insert(0, "BOGA,BOGT")
entry_estaciones.pack()

tk.Label(root, text="Día central (usualmente 6)").pack()
entry_dia = tk.Entry(root, width=5)
entry_dia.insert(0, "6")
entry_dia.pack()

tk.Label(root, text="Ruta archivo Excel con coordenadas").pack()
entry_excel = tk.Entry(root, width=50)
entry_excel.insert(0, "coordenadas_extraidas.xlsx")
entry_excel.pack()

tk.Label(root, text="Carpeta de salida de gráficas").pack()
entry_salida = tk.Entry(root, width=50)
entry_salida.insert(0, "graficas_salida")
entry_salida.pack()

# --- Botones ---
tk.Button(root, text="1️. Descargar GPS y GLONASS", command=ejecutar_descarga_gps_glonass).pack(pady=4)
tk.Button(root, text="2️. Descargar CRD SIRGAS", command=ejecutar_descarga_crd_sirgas).pack(pady=4)
tk.Button(root, text="3️. Descargar CRD IGAC", command=ejecutar_descarga_crd_igac).pack(pady=4)
tk.Button(root, text="4️. Analizar estaciones", command=ejecutar_analisis_estaciones).pack(pady=4)
tk.Button(root, text="5️. Extraer coordenadas de HTML", command=ejecutar_extraccion_coordenadas).pack(pady=4)
tk.Button(root, text="6️. Generar gráficas de desplazamiento", command=ejecutar_graficas_desplazamiento).pack(pady=4)

root.mainloop()

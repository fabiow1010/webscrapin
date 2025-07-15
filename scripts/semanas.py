from ftplib import FTP
import os

def descargar_crd_semanas(semanas, ruta_base_descargas="descargas"):
    """
    Descarga archivos .crd de SIRGAS para las semanas especificadas.

    Args:
        semanas (list[int]): Lista de semanas (como enteros) a descargar.
        ruta_base_descargas (str): Carpeta base donde se guardarán los archivos.
    """
    # Conexión anónima a SIRGAS
    try:
        ftp = FTP('ftp.sirgas.org')
        ftp.login()
        print("Conectado a SIRGAS.")
    except Exception as e:
        print(f"Error al conectar a SIRGAS: {e}")
        return

    print("Semanas a descargar:", len(semanas))

    ruta_base_descargas = os.path.abspath(ruta_base_descargas)
    os.makedirs(ruta_base_descargas, exist_ok=True)

    print("📂 Listando semanas disponibles en SIRGAS...")
    for semana in semanas:
        semana_str = str(semana)  # Convertir a string para usar en rutas y nombres
        print(f"\n📂 Procesando semana {semana_str}...")

        try:
            ftp.cwd(f'/pub/gps/SIRGAS/{semana_str}/')
            archivos = ftp.nlst()
            archivo_crd = next((a for a in archivos if semana_str in a and a.endswith('.crd')), None)

            if archivo_crd:
                print(f"📥 Descargando archivo: {archivo_crd}")
                carpeta_semana = os.path.join(ruta_base_descargas, semana_str)
                os.makedirs(carpeta_semana, exist_ok=True)

                ruta_archivo = os.path.join(carpeta_semana, archivo_crd)
                with open(ruta_archivo, 'wb') as f:
                    ftp.retrbinary(f'RETR {archivo_crd}', f.write)
            else:
                print(f"❌ No se encontró archivo .crd para la semana {semana_str}")

            ftp.cwd('/')

        except Exception as e:
            print(f"❌ No se pudo acceder a la semana {semana_str}: {e}")
            continue

    ftp.quit()
    print("\n✅ Descarga finalizada.")

#Ejemplo de uso:
#semanas = [2325, 2326, 2327]  # Lista de semanas como enteros
#descargar_crd_semanas(semanas)

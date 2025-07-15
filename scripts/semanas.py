from ftplib import FTP
import os

def descargar_crd_semanas(semanas, ruta_base_descargas="descargas"):
    """
    Descarga archivos .crd de SIRGAS para las semanas especificadas.

    Args:
        semanas (list): Lista de semanas a descargar.
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

    ftp.quit()
    print("\n✅ Descarga finalizada.")

#Ejemplo de uso:
semanas = ["2327", "2328", "2329", "2330", "2331", "2335", "2336", "2337", "2338"]
descargar_crd_semanas(semanas)

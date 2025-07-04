import os
import gzip
import requests
from datetime import datetime, timedelta
from unlzw3 import unlzw

def expandir_dias_con_rolldown(semanas, dia_central):
    pares = []
    for semana in semanas:
        for d in [-1, 0, 1]:
            dia = dia_central + d
            if dia < 0:
                pares.append((semana - 1, 6))
            elif dia > 6:
                pares.append((semana + 1, 0))
            else:
                pares.append((semana, dia))
    return pares

def get_julian_day(year, week, dow):
    gps_start = datetime(1980, 1, 6)
    date = gps_start + timedelta(weeks=week, days=dow)
    year = date.strftime("%Y")
    doy = date.strftime("%j")
    return year + doy + "0000", date

def descomprimir_gz(ruta_entrada):
    if ruta_entrada.endswith(".gz"):
        ruta_salida = ruta_entrada[:-3]
        try:
            with gzip.open(ruta_entrada, 'rb') as f_in:
                with open(ruta_salida, 'wb') as f_out:
                    f_out.write(f_in.read())
            print(f"🗃️ Descomprimido: {ruta_salida}")
            os.remove(ruta_entrada)
        except Exception as e:
            print(f"⚠️ Error descomprimiendo {ruta_entrada}: {e}")

def descomprimir_lzw_z(ruta_entrada):
    if ruta_entrada.endswith(".Z"):
        ruta_salida = ruta_entrada[:-2]
        try:
            with open(ruta_entrada, 'rb') as f_in:
                data = unlzw(f_in.read())
            with open(ruta_salida, 'wb') as f_out:
                f_out.write(data)
            print(f"🗃️ Archivo descomprimido: {ruta_salida}")
            os.remove(ruta_entrada)
        except Exception as e:
            print(f"⚠️ Error al descomprimir {ruta_entrada}: {e}")

def descargar_GPS(weeks, dia_central):
    base_url = "https://cddis.nasa.gov/archive/gnss/products"
    pares = expandir_dias_con_rolldown(weeks, dia_central)
    base_path = os.path.join(os.getcwd(), "descargas")

    session = requests.Session()
    session.headers.update({'User-Agent': 'nasa-client'})

    for week, day in pares:
        folder = os.path.join(base_path, str(week))
        os.makedirs(folder, exist_ok=True)

        fecha_str, date = get_julian_day(2024, week, day)
        filename = f"IGS0OPSRAP_{fecha_str}_01D_15M_ORB.SP3.gz"
        url = f"{base_url}/{week}/{filename}"
        save_path = os.path.join(folder, filename)

        print(f"🔄 Descargando: {url}")
        try:
            r = session.get(url, stream=True, timeout=30)
            if r.status_code == 200:
                with open(save_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"✅ Guardado: {save_path}")
                descomprimir_gz(save_path)
            else:
                print(f"❌ {r.status_code} al descargar: {url}")
                print(r.text[:200])
        except Exception as e:
            print(f"⚠️ Error: {e}")

def descargar_glonass(weeks, dia_central):
    base_url = "https://cddis.nasa.gov/archive/glonass/products/"
    pares = expandir_dias_con_rolldown(weeks, dia_central)
    base_path = os.path.join(os.getcwd(), "descargas")

    session = requests.Session()
    session.headers.update({'User-Agent': 'nasa-client'})

    tipos = ["sp3"]
    centros = ["igl"]

    for week, day in pares:
        folder = os.path.join(base_path, str(week))
        os.makedirs(folder, exist_ok=True)

        for centro in centros:
            for tipo in tipos:
                filename = f"{centro}{week}{day}.{tipo}.Z"
                url = f"{base_url}/{week}/{filename}"
                save_path = os.path.join(folder, filename)

                print(f"🔄 Descargando: {url}")
                try:
                    r = session.get(url, stream=True, timeout=30)
                    if r.status_code == 200:
                        with open(save_path, "wb") as f:
                            for chunk in r.iter_content(chunk_size=8192):
                                f.write(chunk)
                        print(f"✅ Guardado: {save_path}")
                        descomprimir_lzw_z(save_path)
                    else:
                        print(f"❌ No encontrado ({r.status_code}): {url}")
                        print(r.text[:200])
                except Exception as e:
                    print(f"⚠️ Error al descargar {url}: {e}")

# Ejecución
semanas = [2327, 2328]
dia_central = 6  # sábado
descargar_GPS(semanas, dia_central)
descargar_glonass(semanas, dia_central)

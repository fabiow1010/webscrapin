import os
import gzip
import requests
from datetime import datetime, timedelta

def get_julian_day(year, week, dow):
    gps_start = datetime(1980, 1, 6)
    date = gps_start + timedelta(weeks=week, days=dow)
    year = date.strftime("%Y")
    doy = date.strftime("%j")
    return year + doy + "0000", date

def descomprimir_gz(ruta_entrada):
    if ruta_entrada.endswith(".gz"):
        ruta_salida = ruta_entrada[:-3]  # quita .gz
        try:
            with gzip.open(ruta_entrada, 'rb') as f_in:
                with open(ruta_salida, 'wb') as f_out:
                    f_out.write(f_in.read())
            print(f"🗃️ Descomprimido: {ruta_salida}")
            os.remove(ruta_entrada)
        except Exception as e:
            print(f"⚠️ Error descomprimiendo {ruta_entrada}: {e}")

def descargar_archivos_modernos(weeks, dia_central):
    base_url = "https://cddis.nasa.gov/archive/gnss/products"
    dias = [dia_central - 1, dia_central, dia_central + 1]
    dias = [d for d in dias if 0 <= d <= 6]
    base_path = os.path.join(os.getcwd(), "descargas") 

    session = requests.Session()
    session.headers.update({'User-Agent': 'nasa-client'})

    for week in weeks:
        folder = os.path.join(base_path, str(week))
        os.makedirs(folder, exist_ok=True)

        for day in dias:
            fecha_str, date = get_julian_day(2024, week, day)
            # Nombre del archivo según el nuevo estándar
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

# Configuración
semanas = [2327, 2328]
dia_central = 3  # miércoles

descargar_archivos_modernos(semanas, dia_central)

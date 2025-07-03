import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

def get_adjacent_days(day_input):
    day_input = int(day_input)
    days = set([day_input])
    if day_input > 0:
        days.add(day_input - 1)
    if day_input < 6:
        days.add(day_input + 1)
    return sorted(list(days))

def descargar_archivos(weeks, dia_central, username, password):
    base_url = "https://cddis.nasa.gov/archive/gnss/products"
    session = requests.Session()
    session.auth = HTTPBasicAuth(username, password)
    session.headers.update({'User-Agent': 'NASA Downloader'})

    dias = get_adjacent_days(dia_central)

    base_path = os.path.join(os.getcwd(), "descargas") 

    for week in weeks:
        folder = os.path.join(base_path, str(week))  # Carpeta: descargas/1185/
        os.makedirs(folder, exist_ok=True)

        for day in dias:
            for prefix in ["igs", "igl"]:
                filename = f"{prefix}{week}{day}.sp3.Z"
                url = f"{base_url}/{week}/{filename}"
                save_path = os.path.join(folder, filename)
                print(f"🔄 Descargando: {url}")
                try:
                    response = session.get(url, stream=True, timeout=30)
                    if response.status_code == 200:
                        with open(save_path, "wb") as f:
                            for chunk in response.iter_content(chunk_size=8192):
                                f.write(chunk)
                        print(f"✅ Guardado: {save_path}")
                    else:
                        print(f"❌ No encontrado ({response.status_code}): {url}")
                except Exception as e:
                    print(f"⚠️ Error al descargar {url}: {e}")


semanas = [1185, 1186]
dia_central = 3 


load_dotenv()
usuario = os.getenv("USUARIO")
contraseña = os.getenv("CONTRASEÑA")

descargar_archivos(semanas, dia_central, usuario, contraseña)
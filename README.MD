


# GNSS FabiDev

Este proyecto permite **descargar, procesar y analizar archivos de efemérides GNSS y coordenadas de estaciones**, integrando varios scripts en Python para automatizar todo el flujo de trabajo.


## 📁 Estructura del proyecto

La estructura mínima de carpetas esperada por los scripts es la siguiente:

```

GNSS-FabiDev/
│
├── .venv/                         # Entorno virtual (no incluido en el repo)
├── descargas/                    # Carpeta donde se guardan descargas por semana
│   └── reportes/                # HTMLs de reportes de coordenadas (agregados manualmente)
├── ejemplo/                      # Ejemplos de archivos o plantillas
├── graficas\_salida/             # Carpeta de salida para gráficos finales
├── scripts/                     # Scripts principales
│   ├── index.py
│   ├── script.py
│   ├── semanas.py
│   └── ...
├── .gitignore
├── cookies.txt                  # (si aplica) Cookies para autenticación
├── coordenadas\_extraidas.csv   # Resultado de análisis de coordenadas
├── coordenadas\_extraidas.xlsx  # Versión Excel de las coordenadas
├── requeriments.txt            # Requisitos del proyecto
└── README.MD
```


> ⚠️ **Nota importante:** Algunas carpetas como `descargas`, `graficas_salida` y `descargas/reportes` no se incluyen en el repositorio por defecto. **Deben ser creadas manualmente** o se crearán automáticamente durante la ejecución del script.


## ⚙️ Requisitos

- Python 3.x
- Paquetes:
  - `requests`
  - `pandas`
  - `numpy`
  - `matplotlib`
  - `ftplib`

Instalación:

```bash
pip install -r requeriments.txt
````



## 🛠️ Configuración inicial

1. **(Obligatorio)** Crear un archivo `.env` en la raiz de proyecto para almacenar credenciales de descarga de CDDIS/NASA:

   ```bash
   USUARIO=tu_usuario
   CONTRASENA=tu_contraseña
   ```

2. Asegúrate de tener la siguiente estructura de carpetas antes de ejecutar:

   * `descargas/`: Se crearán subcarpetas por semana con los archivos descargados.
   * `descargas/reportes/`: Agrega aquí los archivos HTML de reporte manualmente.
   * `graficas_salida/`: Aquí se guardarán los gráficos generados.
   * `scripts/`: Contiene los scripts principales de ejecución.

3. Abre `scripts/index.py` y ajusta:

   * Las semanas a procesar (`semanas`)
   * Días de la semana (0-6) del procesamiento(`dia_central`)
   * Las estaciones base (`estaciones`)
   * La ruta del archivo Excel de entrada o salida, si aplica.



## ▶️ Ejecución

### Opción 1: Flujo automatizado

El script `index.py` ejecuta todo el flujo: descarga de efemérides, descarga de CRD, análisis de estaciones y generación de gráficos.

```bash
python scripts/index.py
```



### Opción 2: Ejecuciones parciales

Puedes ejecutar partes específicas según el script que necesites:

#### a. Descarga de archivos SP3

```bash
python scripts/script.py
```

#### b. Descarga de archivos `.crd` (desde SIRGAS e IGAC)

```bash
python scripts/semanas.py
```

#### c. Análisis de estaciones base

```bash
python scripts/analisis.py
```

#### d. Generación de gráficas desde archivo Excel

```bash
python scripts/deslpazamientos.py
```

---

## 📊 Resultados esperados

* Archivos SP3, GLONASS y `.crd` organizados por semana en `descargas/`
* Archivo `DATA.csv` con las coordenadas procesadas de las estaciones base
* Gráficos de desplazamiento (`.png`) por estación en `graficas_salida/`
* Coordenadas extraídas desde HTMLs en `coordenadas_extraidas.xlsx`

---

## ⚠️ Notas adicionales

* Asegúrate de tener conexión a internet para realizar las descargas.
* Algunas fuentes requieren **credenciales válidas** (como CDDIS/NASA).
* Verifica que tengas **permisos de escritura** en las carpetas de trabajo.
* Los comentarios en los scripts te orientarán para hacer ajustes personalizados (por ejemplo, nombre de columnas en el Excel, estaciones específicas, rutas, etc.).
* Se encuentra en etapa de desarrollo una interfaz mediante Tkinter que pérmita llevar el flujo de trabajo del el alistamiento de datos para levantamientos GNSS de una manera mas interactiva, se recomienda discresión con su uso.

# GNSS FabiDev

Este proyecto permite descargar, procesar y analizar archivos de efemérides GNSS y coordenadas de estaciones, integrando scripts para automatizar todo el flujo de trabajo.

## Estructura de carpetas

- `scripts/`: Scripts principales (`index.py`, `script.py`, `semanas.py`).
- `descargas/`: Archivos SP3 descargados.
- `salidas/`: Archivos `.crd`, resultados procesados y gráficos generados.
- `config/`: Archivos de configuración (por ejemplo, credenciales y parámetros).
- `requeriments.txt`: Lista de dependencias.

## Requisitos

- Python 3.x
- Paquetes: `requests`, `pandas`, `numpy`, `matplotlib`, `ftplib`

Instala los paquetes necesarios con:

```bash
pip install -r requeriments.txt
```

## Configuración inicial

1. Crea un archivo `.env` en la carpeta `scripts`, allí deben estar las credenciales, usuario y contraseña de acceso a CDDIS/NASA:
   1. 
   ```bash
   USUARIO=username
    CONTRASENA=password
   ```
2. Crea la carpeta `descargas/` y dentro de ella la carpeta `\reportes`
   - En la carpeta de descargas se generan los archivos de salida de las semanas
   - En la caepta de reportes deben agregar manualmente los reportes de procesamiento de los puntos levantamos.

3. Edita `scripts/index` para definir:
    - Semanas a procesar.
    - Bases .
    - Parámetros de estaciones y rutas.

## Ejecución del sistema

### 1. Flujo automatizado con `index.py`

`index.py` coordina la descarga y análisis de archivos SP3 y `.crd` en un solo paso.

**Uso:**

```bash
python scripts/index.py
```

El script lee la descripción en cada directorio, descarga los archivos necesarios y genera los resultados en `descargas/`.

### 2. Descarga manual de archivos SP3 (`script.py`)

Descarga archivos SP3 comprimidos desde CDDIS/NASA para semanas y días específicos.

**Uso:**

1. Edita las variables en `.env`.
2. Ejecuta:

```bash
python scripts/script.py
```

Archivos descargados se guardan en `descargas/`.

### 3. Descarga y análisis de archivos `.crd` (`semanas.py`)

Conecta al FTP de SIRGAS, descarga archivos `.crd` y analiza la estación BOGA.

**Uso:**

1. Edita la lista de semanas en `semanas.py` o usa la configuración de ejemplo.
2. Ejecuta:

```bash
python scripts/semanas.py
```

Resultados y gráficos se guardan en `descargas/`.

## Resultados

- Archivos SP3 y `.crd` organizados por semana.
- Archivo `DATA.csv` con datos procesados de la estación BOGA.
- Gráficos de evolución de coordenadas en `descargas/`.

---

**Notas:**
- Requiere conexión a internet.
- Credenciales válidas para CDDIS/NASA.
- Permisos de escritura en carpetas de destino.
- Consulta los comentarios en cada script para personalizaciones avanzadas.

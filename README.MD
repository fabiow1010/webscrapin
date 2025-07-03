# GNSS FabiDev
Este proyecto contiene scripts para descargar y analizar archivos de efemérides y coordenadas GNSS.

## Estructura de carpetas

- `scripts/`: Contiene los scripts principales.
- `descargas/`: Carpeta donde se guardan los archivos descargados por `script.py`.
- `salidas/`: Carpeta donde se guardan los archivos .crd y resultados procesados por `semanas.py`.

## Requisitos

- Python 3.x
- Paquetes: `requests`, `pandas`, `numpy`, `matplotlib`

Instala los paquetes necesarios con:

```
pip install requests pandas numpy matplotlib
```
o con:
```
pip install -r requeriments.txt
```
## Ejecución de scripts

### 1. Descargar archivos SP3 de efemérides (CDDIS/NASA)

El script `scripts/script.py` descarga archivos SP3 comprimidos (`.sp3.Z`) de efemérides GNSS desde el servidor de CDDIS/NASA para semanas y días específicos.

**Uso:**

1. Edita las variables `semanas`, `dia_central`, `usuario` y `contraseña` en `script.py` según tus necesidades.
2. Ejecuta el script:

```
python scripts/script.py
```

Los archivos descargados se guardarán en la carpeta `descargas/` organizada por semana.

### 2. Descargar y analizar archivos .crd de SIRGAS

El script `scripts/semanas.py` se conecta al servidor FTP de SIRGAS, descarga archivos `.crd` de coordenadas para las semanas especificadas y realiza un análisis de la estación BOGA.

**Uso:**

1. Edita la lista `semanas` en `semanas.py` si deseas otras semanas.
2. Ejecuta el script:

```
python scripts/semanas.py
```

Esto descargará los archivos `.crd` a la carpeta `salidas/`, generará un archivo `DATA.csv` con los datos de la estación BOGA y mostrará gráficos de los cambios en coordenadas.

---

**Nota:**
- Asegúrate de tener conexión a internet.
- Para el script de CDDIS/NASA necesitas usuario y contraseña válidos para CDDIS.
- Los scripts pueden requerir permisos de escritura en las carpetas de destino.
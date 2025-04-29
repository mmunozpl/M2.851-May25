# M2851-Mar25
Tipología y ciclo de vida de los datos PRA1 UOC Mar2025

# BOE Data Scraper

Scraper en Python para extraer anuncios de licitaciones y contrataciones diarias publicadas en el Boletín Oficial del Estado (BOE) a lo largo de un período definido de 10 años (2014–2024). El proceso se organiza de forma modular y el dataset resultante se guarda en el directorio `CSV`.

## Estructura del Proyecto
```
. 
├── CSV
│   ├── LICENSE_dataset.txt 
│   └── licitaciones_contrataciones_BOE_2014_2024.csv
├── LICENSE.txt 
├── LICENSE_dataset.txt 
├── README.md 
├── requirements.txt 
└── source 
    ├── get_session.py 
    ├── obtener_analisis.py 
    ├── obtener_extra_texto.py 
    ├── obtener_datos_economicos.py
    ├── obtener_anuncios.py 
    └── main.py
```
## Descripción del Código

El proceso se organiza en cinco apartados:

- **Extracción y procesamiento de los anuncios diarios – función `obtener_anuncios`**  
  - Convierte la fecha al formato `dd/mm/aaaa`
  - Solicita la página diaria del BOE y, en caso de error, salta ese día sin interrumpir el flujo
  - Extrae los datos básicos para cada anuncio (`<li class="dispo">`) como institución, organismo responsable, objeto, expediente, enlace HTML y tipo preliminar (licitación o contratación)
  - Llama a `obtener_analisis`, `obtener_extra_texto` y `obtener_datos_economicos_y_nif` para enriquecer el anuncio con campos adicionales

- **Extracción de la sección “ANÁLISIS” – función `obtener_analisis`**  
  - Extrae Modalidad, Tipo, Procedimiento, Ámbito geográfico, Materias CPV y Observaciones

- **Extracción adicional del texto – función `obtener_extra_texto`**  
  - Extrae campos como `Codigos_CPV` desde la sección detallada del texto

- **Extracción de NIFs y valores económicos – función `obtener_datos_economicos_y_nif`**  
  - Extrae desde bloques anidados los siguientes campos:
    - `nif_licitador`, `valor_estimado_licitacion`
    - `nombre_poder_adjudicador`, `nif_adjudicador`
    - `nombre_adjudicatario`, `nif_adjudicatario`
    - `valor_oferta_adjudicada`

- **Generación del DataFrame y exportación – `main.py`**  
  - Define el rango de fechas y llama a `obtener_anuncios` día por día
  - Aplica un `delay` entre solicitudes
  - Añade una columna de verificación (`verificacion_organismo`) que compara `Organismo responsable` y `nombre_poder_adjudicador`
  - Exporta el resultado a `datos/boe/` y a `CSV/` como `licitaciones_contrataciones_BOE_2014_2024.csv`

### Atributos del dataset

- **Institucion**
- **Organismo responsable**
- **Expediente**
- **Fecha**
- **Tipo**
- **Objeto**
- **Modalidad**
- **Procedimiento**
- **Ambito_geografico**
- **Materias_CPV**
- **codigos_CPV**
- **nif_licitador**
- **valor_estimado_licitacion**
- **nombre_poder_adjudicador**
- **nif_adjudicador**
- **nombre_adjudicatario**
- **nif_adjudicatario**
- **valor_oferta_adjudicada**
- **verificacion_organismo**
- **Enlace HTML**

## Buenas Prácticas y Consideraciones Éticas

- **Persistencia de conexión** con `requests.Session()`
- **Timeouts y reintentos** configurados
- **Delay configurable** entre peticiones para no sobrecargar el servidor
- **Modularidad**: cada función en su archivo
- **Gestión de errores** para permitir ejecución continua
- **Verificación cruzada** entre fuentes de datos (`verificacion_organismo`)

## Requisitos

- Python 3.9  
- Las siguientes librerías (instalables vía `pip install -r requirements.txt`):
  - `requests == 2.31.0`
  - `urllib3 == 2.2.3`
  - `beautifulsoup4 == 4.12.3`
  - `pandas == 2.0.3`

## Uso

Para ejecutar el scraper, sitúate en el directorio raíz y lanza:

```bash
python source/main.py
```
El CSV final se generará en `CSV/licitaciones_contrataciones_BOE_2014_2024.csv`
```

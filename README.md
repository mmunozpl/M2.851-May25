<h1>BOE Data Scraper</h1>
<p><strong>Tipología y ciclo de vida de los datos UOC Mar2025</strong></p>

<p>Scraper en Python para extraer anuncios de licitaciones y contrataciones diarias publicadas en el Boletín Oficial del Estado (BOE) a lo largo de un período definido de 10 años (2014–2024). El proceso se organiza de forma modular y el dataset resultante se guarda en el directorio <code>CSV</code>.</p>

<p>Sitio del autor: <a href="https://manpla.net/perfil">manpla.net</a> · publicaciones: <a href="https://manpla.net/papers">manpla.net/papers</a></p>

<h2>Estructura del Proyecto</h2>
<pre><code>.
├── Analisis R
│   ├── CSV
│   ├── M2.851_20241_May25.V.1.7.Rmd   # Notebook principal de análisis en R
│   ├── M2.851_20241_May25.V.1.7.pdf   # Informe generado en PDF
│   └── ... (otros archivos auxiliares de R)
├── CSV
│   ├── LICENSE_dataset.txt
│   ├── licitaciones_contrataciones_BOE_2014_2024.csv
│   └── licitaciones_contrataciones_BOE_2014_2024_test.csv
├── source
│   ├── __init__.py
│   ├── estadistica.py
│   ├── get_session.py
│   ├── main.py
│   ├── obtener_analisis.py
│   ├── obtener_anuncios.py
│   ├── obtener_datos_economicos.py
│   ├── obtener_extra_texto.py
│   └── test.py
├── LICENSE
├── LICENSE_dataset.txt
├── README.md
├── requirements.txt
└── .gitattributes
</code></pre>

<h2>Descripción del Código</h2>
<ul>
  <li><strong>obtener_anuncios:</strong> obtiene datos básicos y llama a los módulos auxiliares</li>
  <li><strong>obtener_analisis:</strong> extrae modalidad, tipo, procedimiento, ámbito, materias y observaciones</li>
  <li><strong>obtener_extra_texto:</strong> extrae <code>Codigos_CPV</code></li>
  <li><strong>obtener_datos_economicos:</strong> extrae adjudicatarios y valores desde texto plano, listas y bloques</li>
  <li><strong>main.py:</strong> orquesta el scraping completo y guarda el CSV</li>
  <li><strong>test.py:</strong> pruebas de funcionamiento y verificación de los módulos</li>
</ul>

<h3>Atributos del dataset</h3>
<ul>
  <li>Institucion</li>
  <li>Organismo responsable</li>
  <li>Expediente</li>
  <li>Fecha</li>
  <li>Tipo</li>
  <li>Objeto</li>
  <li>Procedimiento</li>
  <li>Ambito_geografico</li>
  <li>Naturaleza (nuevo)</li>
  <li>Materias_CPV</li>
  <li>Codigos_CPV</li>
  <li>valor_estimado_licitacion (nuevo)</li>
  <li>valor_oferta_adjudicada (nuevo)</li>
  <li>nombre_adjudicatario (nuevo)</li>
  <li>Enlace HTML</li>
</ul>

<h2>Buenas Prácticas y Ética</h2>
<ul>
  <li>Conexión persistente con <code>requests.Session()</code></li>
  <li>Timeouts y reintentos por defecto</li>
  <li>Retrasos configurables entre peticiones</li>
  <li>Manejo robusto de errores</li>
  <li>Visualización de adjudicatarios por consola</li>
</ul>

<h2>Requisitos</h2>
<p>Python 3.9+ y las siguientes dependencias:</p>
<pre><code>requests==2.31.0
urllib3==2.2.3
beautifulsoup4==4.12.3
pandas==2.0.3
</code></pre>

<h2>Uso</h2>
<p>Desde el directorio raíz del proyecto:</p>
<pre><code>python source/main.py</code></pre>

<p>El archivo CSV final estará en:</p>
<pre><code>CSV/licitaciones_contrataciones_BOE_2014_2024.csv</code></pre>

<h2>Disponibilidad del Dataset</h2>
<ul>
  <li><strong>Zenodo (DOI):</strong> <a href="https://doi.org/10.5281/zenodo.18712463">10.5281/zenodo.18712463</a> — <a href="https://doi.org/10.5281/zenodo.15117890">10.5281/zenodo.15117890</a> (DOI de concepto, siempre apunta a la última versión)</li>
  <li><strong>Hugging Face:</strong> <a href="https://huggingface.co/datasets/ManPla/licitaciones-contrataciones-boe-2014-2024">ManPla/licitaciones-contrataciones-boe-2014-2024</a></li>
  <li><strong>Autor:</strong> Manuel Muñoz Plá — ORCID: <a href="https://orcid.org/0009-0000-5714-912X">0009-0000-5714-912X</a></li>
</ul>

<h2>Cómo citar</h2>
<p>Si mencionas o usas esta obra, cítala así (GitHub también ofrece el botón «Cite this repository», generado desde <code>CITATION.cff</code>):</p>
<pre><code>Muñoz Plá, M. (2026). Licitaciones y Contrataciones del BOE (2014–2024) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.18712463</code></pre>

<pre><code>@dataset{munozpla2026licitacionesboe,
  author    = {Muñoz Plá, Manuel},
  title     = {Licitaciones y Contrataciones del BOE (2014–2024)},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.18712463},
  url       = {https://doi.org/10.5281/zenodo.18712463}
}</code></pre>

</body>
</html>

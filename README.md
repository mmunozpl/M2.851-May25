<h1>BOE Data Scraper</h1>
<p><strong>Tipología y ciclo de vida de los datos PRA2 UOC Mar2025</strong></p>

<p>Scraper en Python para extraer anuncios de licitaciones y contrataciones diarias publicadas en el Boletín Oficial del Estado (BOE) a lo largo de un período definido de 10 años (2014–2024). El proceso se organiza de forma modular y el dataset resultante se guarda en el directorio <code>CSV</code>.</p>

<h2>Estructura del Proyecto</h2>
<pre><code>.
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
    ├── main.py
    └── __init__.py
</code></pre>

<h2>Descripción del Código</h2>
<ul>
  <li><strong>obtener_anuncios:</strong> obtiene datos básicos y llama a los módulos auxiliares</li>
  <li><strong>obtener_analisis:</strong> extrae modalidad, tipo, procedimiento, ámbito, materias y observaciones</li>
  <li><strong>obtener_extra_texto:</strong> extrae <code>Codigos_CPV</code></li>
  <li><strong>obtener_datos_economicos:</strong> extrae adjudicatarios y valores desde texto plano, listas y bloques</li>
  <li><strong>main.py:</strong> orquesta el scraping completo y guarda el CSV</li>
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
  <li>Materias_CPV</li>
  <li>Codigos_CPV</li>
  <li>valor_estimado_licitacion</li>
  <li>valor_oferta_adjudicada</li>
  <li>nombre_adjudicatario</li>
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

</body>
</html>

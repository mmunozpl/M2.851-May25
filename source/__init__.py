"""
Módulo de scraping del BOE para anuncios de licitación y contratación.

Este paquete contiene los siguientes submódulos:

- get_session: sesión HTTP reutilizable con cabeceras y reintentos.
- obtener_anuncios: extracción principal de datos diarios del BOE.
- obtener_analisis: análisis estructurado de secciones tipo <dl> en detalle HTML.
- obtener_extra_texto: extracción de códigos CPV y otras menciones relevantes.
- obtener_datos_economicos: análisis económico con adjudicatarios e importes.

Uso típico:
    from source.obtener_anuncios import obtener_anuncios
"""

__all__ = [
    "get_session",
    "obtener_anuncios",
    "obtener_analisis",
    "obtener_extra_texto",
    "obtener_datos_economicos"
]

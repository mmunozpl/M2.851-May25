"""
obtener_anuncios.py
Este módulo define la función obtener_anuncios,
que procesa cada página diaria del BOE para extraer
los anuncios publicados, combinando datos básicos y enriquecidos
"""

import re
from datetime import datetime
from typing import List, Dict
from bs4 import BeautifulSoup
from source.get_session import get_session
from source.obtener_analisis import obtener_analisis
from source.obtener_extra_texto import obtener_extra_texto
from source.obtener_datos_economicos import obtener_datos_economicos

REQUEST_TIMEOUT: int = 3
BASE_URL: str = "https://www.boe.es/boe/dias"

def obtener_anuncios(fecha: str) -> List[Dict[str, str]]:
    try:
        fecha_obj = datetime.strptime(fecha, "%Y/%m/%d")
        fecha_formateada = fecha_obj.strftime("%d/%m/%Y")
    except Exception as e:
        print(f"Error formateando fecha {fecha}: {e}")
        fecha_formateada = fecha

    url: str = f"{BASE_URL}/{fecha}/index.php?l=DA"
    session = get_session()
    try:
        response = session.get(url, timeout=REQUEST_TIMEOUT)
    except Exception as e:
        print(f"Error al conectar con {url}: {e}")
        return []

    if response.status_code != 200:
        print(f"Error {response.status_code} en {url}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    contenido = soup.find('div', id='contenido')
    if not contenido:
        return []

    anuncios: List[Dict[str, str]] = []
    institucion_actual: str = "No disponible"
    for elem in contenido.find_all(['h4', 'li']):
        if elem.name == 'h4':
            institucion_actual = elem.get_text(strip=True)
        elif elem.name == 'li' and 'dispo' in elem.get('class', []):
            p_tag = elem.find('p')
            if not p_tag:
                continue
            texto_anuncio: str = p_tag.get_text(strip=True)

            if "Anuncio de licitación de" in texto_anuncio or "Anuncio de formalización de contratos de" in texto_anuncio:
                tipo_inicial = "Licitación" if "Anuncio de licitación de" in texto_anuncio else "Contratación"

                match_org = re.search(r"Anuncio de (?:licitación|formalización) de contratos de:\s*(.+?)(?:\.|$)", texto_anuncio, re.IGNORECASE)
                organismo = match_org.group(1).strip() if match_org else "No disponible"

                objeto = "No disponible"
                if "Objeto:" in texto_anuncio:
                    partes = texto_anuncio.split("Objeto:")
                    if len(partes) > 1:
                        objeto = partes[1].split("Expediente:")[0].strip()

                expediente = "No disponible"
                if "Expediente:" in texto_anuncio:
                    match_exp = re.search(r"Expediente:\s*([^\n]+)", texto_anuncio)
                    expediente = match_exp.group(1).strip() if match_exp else "No disponible"

                html_link_tag = elem.find('a', href=True, title=lambda x: x and "Versión HTML" in x)
                if not html_link_tag:
                    html_link_tag = elem.find('a', href=re.compile(r'\.html', re.IGNORECASE))
                enlace_html = "https://www.boe.es" + html_link_tag.get("href") if html_link_tag else "No disponible"

                anuncio = {
                    "Institucion": institucion_actual,
                    "Organismo responsable": organismo,
                    "Expediente": expediente,
                    "Fecha": fecha_formateada,
                    "Tipo": tipo_inicial,
                    "Objeto": objeto,
                    "Enlace HTML": enlace_html
                }

                if enlace_html != "No disponible":
                    analisis_data = obtener_analisis(enlace_html)

                    # guardar el tipo de contrato del análisis (Servicios, Obras, etc.) sin interferir con "Tipo"
                    anuncio["Naturaleza"] = analisis_data.get("Tipo", "No disponible")

                    tipo_analisis = analisis_data.get("Tipo", "No disponible")
                    if tipo_analisis in ["Licitación", "Contratación"]:
                        anuncio["Tipo"] = tipo_analisis

                    anuncio["Procedimiento"] = analisis_data.get("Procedimiento", "No disponible")
                    anuncio["Ambito_geografico"] = analisis_data.get("Ambito_geografico", "No disponible")
                    anuncio["Materias_CPV"] = analisis_data.get("Materias_CPV", "No disponible")
                    anuncio["Observaciones"] = analisis_data.get("Observaciones", "No disponible")

                    extra_texto = obtener_extra_texto(enlace_html)
                    anuncio["Codigos_CPV"] = extra_texto.get("Codigos_CPV", "No disponible")

                    if anuncio.get("Organismo responsable", "No disponible") == "No disponible":
                        try:
                            soup_detalle = BeautifulSoup(session.get(enlace_html, timeout=REQUEST_TIMEOUT).text, "html.parser")
                            texto_div = soup_detalle.find("div", id="textoxslt")
                            if texto_div:
                                dts = texto_div.find_all("dt")
                                for dt in dts:
                                    texto_dt = dt.get_text(strip=True).lower()
                                    if texto_dt in ["a) organismo:", "1.1) nombre:"]:
                                        dd = dt.find_next_sibling("dd")
                                        if dd:
                                            organismo_text = dd.get_text(strip=True)
                                            anuncio["Organismo responsable"] = organismo_text
                                            print(f"[INFO] Organismo complementado desde textoxslt: {organismo_text}")
                                            break
                        except Exception as e:
                            print(f"[WARN] No se pudo extraer 'Organismo responsable' desde textoxslt para {enlace_html}: {e}")

                    # pasar el contenido real de anuncio["Tipo"] como guía a obtener_datos_economicos
                    datos_economicos = obtener_datos_economicos(enlace_html, anuncio["Tipo"])
                    if anuncio["Tipo"].lower() == "licitación":
                        anuncio.update(datos_economicos[0])
                        anuncios.append(anuncio)
                    elif anuncio["Tipo"].lower() == "contratación":
                        for entrada in datos_economicos:
                            anuncio_copy = anuncio.copy()
                            anuncio_copy.update(entrada)
                            anuncios.append(anuncio_copy)
                    else:
                        anuncio.update({
                            "valor_estimado_licitacion": "No disponible",
                            "nombre_adjudicatario": "No disponible",
                            "valor_oferta_adjudicada": "No disponible"
                        })
                        anuncios.append(anuncio)
                else:
                    anuncio.update({
                        "Procedimiento": "No disponible",
                        "Ambito_geografico": "No disponible",
                        "Materias_CPV": "No disponible",
                        "Observaciones": "No disponible",
                        "Codigos_CPV": "No disponible",
                        "valor_estimado_licitacion": "No disponible",
                        "nombre_adjudicatario": "No disponible",
                        "valor_oferta_adjudicada": "No disponible"
                    })
                    anuncios.append(anuncio)
    return anuncios

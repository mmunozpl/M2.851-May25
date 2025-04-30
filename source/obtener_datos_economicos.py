import requests
from bs4 import BeautifulSoup


def obtener_datos_economicos_y_nif(enlace_html: str, tipo_anuncio: str) -> dict:
    campos = {
        "nif_licitador": "No disponible",
        "valor_estimado_licitacion": "No disponible",
        "nombre_poder_adjudicador": "No disponible",
        "nif_adjudicador": "No disponible",
        "nombre_adjudicatario": "No disponible",
        "nif_adjudicatario": "No disponible",
        "valor_oferta_adjudicada": "No disponible"
    }
    try:
        response = requests.get(enlace_html, timeout=5)
        if response.status_code != 200:
            return campos
        soup = BeautifulSoup(response.text, 'html.parser')
        texto_div = soup.find('div', id='textoxslt')
        if not texto_div:
            return campos
        dl = texto_div.find('dl')
        if not dl:
            return campos

        dt_actual = None
        for elem in dl.find_all(['dt', 'dd']):
            if elem.name == 'dt':
                dt_actual = elem.get_text(strip=True).lower()
            elif elem.name == 'dd' and dt_actual:
                sub_dl = elem.find('dl')
                if sub_dl:
                    for sub_dt in sub_dl.find_all('dt'):
                        sub_dt_text = sub_dt.get_text(strip=True).lower()
                        sub_dd = sub_dt.find_next_sibling('dd')
                        if not sub_dd:
                            continue
                        sub_dd_text = sub_dd.get_text(strip=True)
                        if tipo_anuncio == "Licitación" and "identificación fiscal" in sub_dt_text:
                            campos["nif_licitador"] = sub_dd_text
                        if tipo_anuncio == "Contratación":
                            if "nombre" in sub_dt_text and "adjudicatario" in dt_actual:
                                campos["nombre_adjudicatario"] = sub_dd_text
                            elif "identificación fiscal" in sub_dt_text and "adjudicatario" in dt_actual:
                                campos["nif_adjudicatario"] = sub_dd_text
                            elif "nombre" in sub_dt_text and "poder adjudicador" in dt_actual:
                                campos["nombre_poder_adjudicador"] = sub_dd_text
                            elif "identificación fiscal" in sub_dt_text and "poder adjudicador" in dt_actual:
                                campos["nif_adjudicador"] = sub_dd_text
                else:
                    dd_text = elem.get_text(strip=True)
                    if tipo_anuncio == "Licitación" and "valor estimado" in dt_actual:
                        campos["valor_estimado_licitacion"] = dd_text
                    if tipo_anuncio == "Contratación" and "oferta seleccionada" in dt_actual:
                        campos["valor_oferta_adjudicada"] = dd_text
    except Exception as e:
        print(f"Error extrayendo datos económicos/NIF de {enlace_html}: {e}")
    return campos

"""
obtener_datos_economicos.py
Este módulo define la función obtener_datos_economicos,
que extrae información complementaria añadiendo 3 nuevos atributos
"valor_estimado_licitacion","valor_oferta_adjudicada", "nombre_adjudicatario",
de cada página detallada del anuncio del BOE
"""
from typing import List, Dict
from bs4 import BeautifulSoup
import requests
import re

def obtener_datos_economicos(enlace_html: str, modalidad: str) -> List[Dict[str, str]]:
    resultados: List[Dict[str, str]] = []
    try:
        response = requests.get(enlace_html, timeout=5)
        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        texto_div = soup.find('div', id='textoxslt')
        if not texto_div:
            return []

        texto = texto_div.get_text(separator='\n', strip=True)

        # LICITACIÓN – valor estimado
        valor_estimado = "No disponible"
        match_estimado = re.search(r"(?i)(?:valor estimado|valor estimado del contrato)[:\s]*([\d.,]+\s*euros)", texto)
        if match_estimado:
            valor_estimado = match_estimado.group(1).strip()
        else:
            match_presupuesto = re.search(
                r"(?i)presupuesto base de licitaci[óo]n.*?(importe total[:\s]*)([\d.,]+\s*euros)",
                texto, re.DOTALL)
            if match_presupuesto:
                valor_estimado = match_presupuesto.group(2).strip()

        if modalidad.lower() == "licitación" or modalidad.lower() == "licitacion":
            print(f"[INFO] Licitación: Valor estimado = {valor_estimado}")
            resultados.append({
                "valor_estimado_licitacion": valor_estimado,
                "nombre_adjudicatario": "No disponible",
                "valor_oferta_adjudicada": "No disponible"
            })
            return resultados

        # CONTRATACIÓN – múltiples adjudicatarios desde texto plano
        bloques = re.findall(
            r"(?i)(?:contratista|adjudicatario)[:\s]*([^\n]+).*?(importe total[:\s]*)([\d.,]+\s*euros)",
            texto, re.DOTALL)
        for nombre, _, importe in bloques:
            print(f"[INFO] Contratación (texto): Adjudicatario = {nombre.strip()} | Importe = {importe.strip()}")
            resultados.append({
                "valor_estimado_licitacion": valor_estimado,
                "nombre_adjudicatario": nombre.strip(),
                "valor_oferta_adjudicada": importe.strip()
            })

        # CONTRATACIÓN – estructura en <dl><dt>
        dls = texto_div.find_all('dl')
        for dl in dls:
            items = dl.find_all(['dt', 'dd'])
            nombre = None
            importe = None
            for i, el in enumerate(items):
                texto_dt = el.get_text(strip=True).lower()
                if el.name == 'dt' and 'nombre' in texto_dt:
                    siguiente = items[i+1] if i + 1 < len(items) else None
                    if siguiente and siguiente.name == 'dd':
                        nombre = siguiente.get_text(strip=True)
                if el.name == 'dt' and 'valor de la oferta seleccionada' in texto_dt:
                    siguiente = items[i+1] if i + 1 < len(items) else None
                    if siguiente and siguiente.name == 'dd':
                        importe = siguiente.get_text(strip=True)
                if nombre and importe:
                    print(f"[INFO] Contratación (<dl>): Adjudicatario = {nombre.strip()} | Importe = {importe.strip()}")
                    resultados.append({
                        "valor_estimado_licitacion": valor_estimado,
                        "nombre_adjudicatario": nombre.strip(),
                        "valor_oferta_adjudicada": importe.strip()
                    })
                    nombre, importe = None, None

        # CONTRATACIÓN – estructura en <p class="parrafo">
        if not resultados:
            parrafos = texto_div.find_all('p', class_='parrafo')
            nombre = None
            for i, p in enumerate(parrafos):
                texto_p = p.get_text(strip=True)
                if re.search(r"\d+\.\d+\.?\d*\)?\s*Nombre", texto_p):
                    match = re.search(r"Nombre[:\s]*(.*)", texto_p)
                    if match:
                        nombre = match.group(1).strip()
                if re.search(r"Valor de la oferta seleccionada", texto_p):
                    match = re.search(r"Valor de la oferta seleccionada[:\s]*([\d.,]+\s*euros)", texto_p)
                    if match and nombre:
                        print(f"[INFO] Contratación (<p>): Adjudicatario = {nombre} | Importe = {match.group(1).strip()}")
                        resultados.append({
                            "valor_estimado_licitacion": valor_estimado,
                            "nombre_adjudicatario": nombre,
                            "valor_oferta_adjudicada": match.group(1).strip()
                        })
                        nombre = None

        if not resultados:
            print("[WARN] No se encontraron adjudicatarios válidos.")
            resultados.append({
                "valor_estimado_licitacion": valor_estimado,
                "nombre_adjudicatario": "No disponible",
                "valor_oferta_adjudicada": "No disponible"
            })

    except Exception as e:
        print(f"[ERROR] Error extrayendo datos económicos de {enlace_html}: {e}")
        resultados.append({
            "valor_estimado_licitacion": "No disponible",
            "nombre_adjudicatario": "No disponible",
            "valor_oferta_adjudicada": "No disponible"
        })

    return resultados


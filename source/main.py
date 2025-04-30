"""
main.py
Módulo principal que recorre el período definido, extrae los anuncios
diarios del BOE y genera un DataFrame que se guarda en un archivo CSV
dentro del directorio CSV
"""

import os
import time
from datetime import datetime, timedelta
import pandas as pd
from source.obtener_anuncios import obtener_anuncios

REQUEST_DELAY: int = 3  # segundos

def verificar_organismo(organismo_responsable: str, nombre_poder_adjudicador: str) -> str:
    if organismo_responsable == "No disponible" or nombre_poder_adjudicador == "No disponible":
        return "No comprobado"
    org_responsable = organismo_responsable.lower().strip()
    poder_adjudicador = nombre_poder_adjudicador.lower().strip()
    if org_responsable in poder_adjudicador or poder_adjudicador in org_responsable:
        return "OK"
    else:
        return "No coincide"

def main() -> None:
    """
    Función para extraer los datos diarios del BOE y generar el CSV final
    """
    # Se define el período: del 1 de enero de 2014 al 31 de diciembre de 2024
    start_date = datetime(2014, 1, 1)
    end_date = datetime(2024, 12, 31)
    todos_anuncios = []
    current_date = start_date

    while current_date <= end_date:
        fecha_str = current_date.strftime("%Y/%m/%d")
        lista = obtener_anuncios(fecha_str)
        print(f"Obtenidos {len(lista)} anuncios del BOE del día {fecha_str}")
        todos_anuncios.extend(lista)
        current_date += timedelta(days=1)
        time.sleep(REQUEST_DELAY)

    df = pd.DataFrame(todos_anuncios)

    # Verificación de coincidencia entre organismo responsable y poder adjudicador
    df["verificacion_organismo"] = df.apply(
        lambda row: verificar_organismo(row["Organismo responsable"], row.get("nombre_poder_adjudicador", "No disponible")),
        axis=1
    )

    # Reordenar columnas si existen
    column_order = [
        "Institucion",
        "Organismo responsable",
        "Expediente",
        "Fecha",
        "Tipo",
        "Objeto",
        "Modalidad",
        "Procedimiento",
        "Ambito_geografico",
        "Materias_CPV",
        "codigos_CPV",
        #"Observaciones",
        "nif_licitador",
        "valor_estimado_licitacion",
        "nombre_poder_adjudicador",
        "nif_adjudicador",
        "nombre_adjudicatario",
        "nif_adjudicatario",
        "valor_oferta_adjudicada",
        "verificacion_organismo",
        "Enlace HTML"
    ]

    df = df[[col for col in column_order if col in df.columns]]

    # Guardar versión en carpeta interna de trabajo
    #os.makedirs("datos/boe", exist_ok=True)
    #df.to_csv("CSV/licitaciones_contrataciones_BOE_2014_2024_ampliado.csv", index=False)

    # Guardar también en la carpeta oficial CSV del proyecto
    #project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    #output_dir = os.path.join(project_root, "CSV")
    #os.makedirs(output_dir, exist_ok=True)
    #output_filename = os.path.join(output_dir, "licitaciones_contrataciones_BOE_2014_2024.csv")
    #df.to_csv(output_filename, index=False)

    # Crear carpeta CSV si no existe
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(project_root, "CSV")
    os.makedirs(output_dir, exist_ok=True)

    # Guardar versión ampliada
    output_ampliado = os.path.join(output_dir, "licitaciones_contrataciones_BOE_2014_2024_ampliado.csv")
    df.to_csv(output_ampliado, index=False)

    # Guardar versión estándar
    #output_filename = os.path.join(output_dir, "licitaciones_contrataciones_BOE_2014_2024.csv")
    #df.to_csv(output_filename, index=False)

    print(f"Dataset ampliado guardado en {output_ampliado}")
    #print(f"Dataset oficial guardado en {output_filename}")
    print("Tamaño de dataset:", df.shape)
    print(df.sample(15))

if __name__ == '__main__':
    main()

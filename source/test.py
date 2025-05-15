import os
import random
from datetime import datetime
import pandas as pd
from source.obtener_anuncios import obtener_anuncios
from source.estadistica import analizar_csv


def fechas_aleatorias_por_año(inicio: int, fin: int, muestras_por_año: int = 3) -> list:
    fechas = []
    for año in range(inicio, fin + 1):
        dias = sorted(random.sample(range(1, 366), muestras_por_año))
        for dia in dias:
            try:
                fecha = datetime(año, 1, 1) + pd.Timedelta(days=dia - 1)
                fechas.append(fecha.strftime("%Y/%m/%d"))
            except ValueError:
                continue
    return fechas

def main() -> None:
    print("[INFO] Iniciando prueba rápida de scraping del BOE")

    fechas = fechas_aleatorias_por_año(2014, 2024, 3)
    todos_anuncios = []

    for fecha_str in fechas:
        print(f"[INFO] Obteniendo anuncios para {fecha_str}")
        lista = obtener_anuncios(fecha_str)
        print(f" → {len(lista)} anuncios encontrados")
        todos_anuncios.extend(lista)

    df = pd.DataFrame(todos_anuncios)

    column_order = [
        "Institucion",
        "Organismo responsable",
        "Expediente",
        "Fecha",
        "Tipo",
        "Objeto",
        "Procedimiento",
        "Ambito_geografico",
        "Materias_CPV",
        "Codigos_CPV",
        "Enlace HTML",
        "valor_estimado_licitacion",
        "valor_oferta_adjudicada",
        "nombre_adjudicatario"
    ]
    existing_cols = [col for col in column_order if col in df.columns]
    df = df[existing_cols]

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(project_root, "CSV")
    os.makedirs(output_dir, exist_ok=True)
    output_filename = os.path.join(output_dir, "licitaciones_contrataciones_BOE_2014_2024_test.csv")
    df.to_csv(output_filename, index=False)

    print(f"[INFO] Dataset de prueba guardado en {output_filename}")
    print("Tamaño del dataset de prueba:", df.shape)
    print(df.head(10))

    analizar_csv(output_filename)


if __name__ == '__main__':
    main()

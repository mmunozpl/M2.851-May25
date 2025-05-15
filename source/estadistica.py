import pandas as pd
import os
from rich.console import Console
from rich.table import Table

console = Console()

def analizar_csv(path_csv: str) -> None:
    """
    Realiza un análisis estadístico básico del CSV generado por main.py con salida enriquecida

    Args:
        path_csv (str): Ruta al archivo CSV completo
    """
    if not os.path.exists(path_csv):
        console.print(f"[bold red]ERROR:[/bold red] Archivo no encontrado: {path_csv}")
        return

    df = pd.read_csv(path_csv)
    total = len(df)
    console.print(f"\n[bold cyan]Total de registros:[/bold cyan] {total}")

    # distribución por tipo
    tipo_counts = df['Tipo'].value_counts(dropna=False)
    table_tipo = Table(title="Distribución por Tipo")
    table_tipo.add_column("Tipo")
    table_tipo.add_column("Cantidad", justify="right")
    for tipo, count in tipo_counts.items():
        table_tipo.add_row(str(tipo), str(count))
    console.print(table_tipo)

    # porcentaje de 'No disponible'
    table_nd = Table(title="% de 'No disponible' por atributo")
    table_nd.add_column("Atributo")
    table_nd.add_column("% No disponible", justify="right")
    for col in df.columns:
        if df[col].dtype == object:
            no_disp = df[col].str.lower().eq("no disponible").sum()
            pct = round((no_disp / total) * 100, 2)
            table_nd.add_row(col, f"{pct}%")
    console.print(table_nd)

    # estadísticas económicas
    table_valores = Table(title="Estadísticas económicas (en euros)")
    table_valores.add_column("Campo")
    table_valores.add_column("Media", justify="right")
    table_valores.add_column("Mediana", justify="right")
    table_valores.add_column("Máximo", justify="right")

    for col in ["valor_estimado_licitacion", "valor_oferta_adjudicada"]:
        if col in df.columns:
            extraidos = df[col].str.extract(r"([\d.,]+)")
            extraidos[0] = extraidos[0].str.replace(".", "", regex=False).str.replace(",", ".", regex=False)
            valores = pd.to_numeric(extraidos[0], errors='coerce').dropna()
            if not valores.empty:
                table_valores.add_row(
                    col,
                    f"{valores.mean():,.2f}",
                    f"{valores.median():,.2f}",
                    f"{valores.max():,.2f}"
                )
            else:
                table_valores.add_row(col, "-", "-", "-")
    console.print(table_valores)

if __name__ == "__main__":
    ruta = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), "CSV", "licitaciones_contrataciones_BOE_2014_2024.csv"))
    analizar_csv(ruta)

#ex7 #ex8 #ex9 #ex10
from __future__ import annotations

from pathlib import Path

import pandas as pd


#ex7
def load_tables_to_dfs(engine) -> tuple[pd.DataFrame, pd.DataFrame]:
    try:
        df_movies = pd.read_sql_table("movies", con=engine)
        df_series = pd.read_sql_table("series", con=engine)
        return df_movies, df_series
    except Exception as e:
        raise RuntimeError(f"Erro ao ler tabelas do banco: {e}") from e


#ex9
def classify_rating(rating: float) -> str:
    if rating >= 9.0:
        return "Obra-prima"
    if rating >= 8.0:
        return "Excelente"
    if rating >= 7.0:
        return "Bom"
    return "Mediano"


#ex8 #ex9
def enrich_movies_df(df_movies: pd.DataFrame) -> pd.DataFrame:
    df = df_movies.copy()
    df["categoria"] = df["rating"].apply(classify_rating)
    return df


#ex8
def top_movies_after_filter(df_movies: pd.DataFrame, min_rating: float = 9.0, n: int = 5) -> pd.DataFrame:
    df = df_movies.sort_values("rating", ascending=False)
    df = df[df["rating"] > min_rating]
    return df.head(n)


#ex10
def summary_by_category_and_year(df_movies: pd.DataFrame) -> pd.DataFrame:
    #Linhas = categoria, colunas = year, valores = contagem de filmes.
    return (
        df_movies.pivot_table(
            index="categoria",
            columns="year",
            values="title",
            aggfunc="count",
            fill_value=0,
        )
        .sort_index()
    )


#ex8
def export_outputs(df_movies: pd.DataFrame, df_series: pd.DataFrame, output_dir: str) -> None:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    try:
        df_movies.to_csv(out / "movies.csv", index=False, encoding="utf-8")
        df_series.to_csv(out / "series.csv", index=False, encoding="utf-8")
        df_movies.to_json(out / "movies.json", orient="records", force_ascii=False, indent=2)
        df_series.to_json(out / "series.json", orient="records", force_ascii=False, indent=2)
    except Exception as e:
        raise RuntimeError(f"Erro ao exportar arquivos: {e}") from e

from __future__ import annotations

from pathlib import Path

from src.config import load_config
from src.scraping import fetch_html, parse_top250
from src.media import Movie, Series
from src.database import (
    create_engine_sqlite, init_db,
    insert_movie, insert_series
)
from src.analysis import (
    load_tables_to_dfs, enrich_movies_df,
    top_movies_after_filter, summary_by_category_and_year,
    export_outputs,
)


def run() -> None:
    config = load_config()

    print("Configurações carregadas:", config)

    # Exercício 1 – baixar HTML
    html = fetch_html(config.imdb_top250_url)

    # Exercício 1/2 – extrair dados
    filmes_top = parse_top250(html, limit=config.n_filmes)

    print(f"Quantidade total coletada: {len(filmes_top)}")
    print("Último filme:", filmes_top[-1])
    print("Primeiro filme:", filmes_top[0])

    # Exibir 10 primeiros títulos
    print("\nPrimeiros 10 títulos do Top 250:")
    primeiros_titulos = filmes_top[:10]
    for f in primeiros_titulos:
        print("•", f.title)

    # Exibir 5 primeiros com formato pedido
    print("\nCinco primeiros com ano e nota:")
    for f in filmes_top[:5]:
        print(f"{f.title} ({f.year}) – Nota: {f.rating:.1f}")

    # Exercício 5 – criar catálogo
    catalogo = []

    for item in filmes_top:
        catalogo.append(
            Movie(title=item.title, year=item.year, rating=item.rating)
        )

    catalogo.append(Series(title="Demo Série Alfa", year=2015, seasons=4, episodes=58))
    catalogo.append(Series(title="Demo Série Beta", year=2019, seasons=2, episodes=20))

    print("\nCatálogo carregado:")
    if len(catalogo) <= 20:
        for midia in catalogo:
            print(midia)
    else:
        for midia in catalogo[:8]:
            print(midia)
        print("... (itens omitidos) ...")
        for midia in catalogo[-2:]:
            print(midia)

    print("\nSéries encontradas:")
    for midia in catalogo:
        if isinstance(midia, Series):
            print(midia)

    # Exercício 6 – banco
    db = create_engine_sqlite(config.db_path)
    init_db(db)

    movies_inseridos = 0
    movies_pulados = 0

    for filme in catalogo:
        if isinstance(filme, Movie):
            inseriu = insert_movie(db, filme.title, filme.year, float(filme.rating))
            movies_inseridos += int(inseriu)
            movies_pulados += int(not inseriu)

    series_inseridas = 0
    series_puladas = 0

    for serie in catalogo:
        if isinstance(serie, Series):
            inseriu = insert_series(db, serie.title, serie.year, serie.seasons, serie.episodes)
            series_inseridas += int(inseriu)
            series_puladas += int(not inseriu)

    print(f"\nBanco atualizado:")
    print(f"Filmes adicionados: {movies_inseridos}, ignorados: {movies_pulados}")
    print(f"Séries adicionadas: {series_inseridas}, ignoradas: {series_puladas}")

    # Exercício 7 – pandas
    df_filmes, df_series = load_tables_to_dfs(db)
    print("\nPrévia dos filmes:")
    print(df_filmes.head())
    print("\nPrévia das séries:")
    print(df_series.head())

    # Exercício 8/9 – enriquecer + top 5
    df_enriquecido = enrich_movies_df(df_filmes)

    print("\nPrimeiros 10 com categoria:")
    print(df_enriquecido[["title", "rating", "categoria"]].head(10))

    melhores = top_movies_after_filter(df_enriquecido, min_rating=9.0, n=5)
    print("\nTop 5 com rating acima de 9.0:")
    print(melhores[["title", "year", "rating", "categoria"]])

    export_outputs(df_enriquecido, df_series, config.output_dir)
    print("\nArquivos exportados com sucesso.")

    # Exercício 10 – resumo
    resumo = summary_by_category_and_year(df_enriquecido)
    print("\nResumo por categoria e ano:")
    print(resumo)


if __name__ == "__main__":
    run()

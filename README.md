# Projeto IMDb – Scraping, Banco de Dados e Análise

Este projeto realiza a coleta dos filmes do IMDb Top 250, armazena os dados em um banco SQLite e gera análises utilizando Pandas. O fluxo completo executado pelo programa é: scraping → banco de dados → análise → exportação dos arquivos.

## Instalação das dependências
Execute no terminal:
pip install -r requirements.txt

## Como executar o projeto
Para rodar todo o fluxo (scraping → inserção no banco → análise):
python -m src.main

Os arquivos resultantes serão salvos automaticamente na pasta "data/".

## Estrutura do Repositório
- README.md — descrição geral do projeto
- requirements.txt — bibliotecas necessárias
- config.json — configurações básicas (ex: URL e caminho do banco)
- .gitignore — arquivos ignorados pelo Git
- src/ — contém todos os módulos Python do projeto
  - main.py
  - scraping.py
  - database.py
  - analysis.py
  - media.py
  - config.py
- data/ — arquivos de saída
  - imdb.db
  - movies.csv
  - series.csv
  - movies.json
  - series.json

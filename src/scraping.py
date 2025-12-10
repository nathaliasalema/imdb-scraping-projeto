from __future__ import annotations

from dataclasses import dataclass
import json
import requests
from bs4 import BeautifulSoup
from collections.abc import Iterable


@dataclass(frozen=True)
class TopMovieRow:
    title: str
    year: int
    rating: float


def _walk_json(obj) -> Iterable[dict]:
    # Percorre objetos aninhados (dict/list) emitindo dicionários
    if isinstance(obj, dict):
        yield obj
        for val in obj.values():
            yield from _walk_json(val)
    elif isinstance(obj, list):
        for val in obj:
            yield from _walk_json(val)


def _parse_via_nextdata(soup: BeautifulSoup, qtd: int) -> list[TopMovieRow]:
    # Fallback usando __NEXT_DATA__
    script_tag = soup.select_one("script#__NEXT_DATA__")
    if not script_tag or not script_tag.string:
        return []

    estrutura = json.loads(script_tag.string)

    encontrados: list[TopMovieRow] = []
    ja_vistos: set[tuple[str, int]] = set()

    for bloco in _walk_json(estrutura):
        titulo = (bloco.get("titleText") or {}).get("text")
        ano = (bloco.get("releaseYear") or {}).get("year")
        nota = (bloco.get("ratingsSummary") or {}).get("aggregateRating")

        if not (titulo and ano and nota):
            continue

        chave = (titulo, int(ano))
        if chave in ja_vistos:
            continue
        ja_vistos.add(chave)

        encontrados.append(
            TopMovieRow(title=str(titulo), year=int(ano), rating=float(nota))
        )

        if len(encontrados) >= qtd:
            break

    return encontrados


def fetch_html(url: str, timeout: int = 30) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
    }
    resposta = requests.get(url, headers=headers, timeout=timeout)
    resposta.raise_for_status()
    return resposta.text


def _required_text(elemento, nome: str) -> str:
    if elemento is None:
        raise ValueError(
            f"Elemento esperado para {nome} não encontrado no HTML (possível mudança no layout)."
        )
    txt = elemento.get_text(" ", strip=True)
    if not txt:
        raise ValueError(
            f"O conteúdo de {nome} está vazio (possível mudança no layout do IMDb)."
        )
    return txt


def parse_top250(html: str, limit: int = 250) -> list[TopMovieRow]:
    soup = BeautifulSoup(html, "html.parser")
    blocos = soup.select("li.ipc-metadata-list-summary-item")

    maximo = min(limit, 250)

    print("DEBUG scraping:")
    print(" - itens detectados no HTML:", len(blocos))
    print(" - tamanho do HTML recebido:", len(html))

    resultado: list[TopMovieRow] = []

    # Tenta extrair primeiro do HTML visível
    for bloco in blocos[:maximo]:
        bruto_titulo = _required_text(bloco.select_one("h3"), "título")
        titulo = bruto_titulo.split(". ", 1)[-1].strip()

        bruto_ano = _required_text(bloco.select_one("span.cli-title-metadata-item"), "ano")
        ano_txt = bruto_ano[:4]
        if not ano_txt.isdigit():
            raise ValueError(f"Ano inválido encontrado: '{bruto_ano}'")
        ano = int(ano_txt)

        bruto_nota = _required_text(bloco.select_one("span.ipc-rating-star--rating"), "nota")
        try:
            nota = float(bruto_nota.replace(",", "."))
        except Exception as exc:
            raise ValueError(f"Valor de nota inválido: '{bruto_nota}'") from exc

        resultado.append(TopMovieRow(title=titulo, year=ano, rating=nota))

    # Se coletou menos que o esperado, usa fallback
    if len(resultado) < maximo:
        print(f"[info] Coletados apenas {len(resultado)} itens; tentando fallback (__NEXT_DATA__).")
        extra = _parse_via_nextdata(soup, qtd=maximo)
        if extra:
            return extra[:maximo]

    # Se não encontrou nada mesmo, levanta erro
    if not blocos and not resultado:
        raise ValueError("Não foi possível localizar itens do Top 250 nem via fallback.")

    return resultado

#ex11
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AppConfig:
    imdb_top250_url: str = "https://www.imdb.com/chart/top/"
    n_filmes: int = 250
    db_path: str = "data/imdb.db"
    output_dir: str = "data"


def load_config(config_path: str | Path = "config.json") -> AppConfig:
    path = Path(config_path)
    if not path.exists():
        return AppConfig()

    with path.open("r", encoding="utf-8") as f:
        raw = json.load(f)

    return AppConfig(
        imdb_top250_url=raw.get("imdb_top250_url", AppConfig.imdb_top250_url),
        n_filmes=int(raw.get("n_filmes", AppConfig.n_filmes)),
        db_path=raw.get("db_path", AppConfig.db_path),
        output_dir=raw.get("output_dir", AppConfig.output_dir),
    )

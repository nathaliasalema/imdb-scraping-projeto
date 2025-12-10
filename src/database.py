#ex6
from __future__ import annotations

from pathlib import Path

from sqlalchemy import Float, Integer, String, UniqueConstraint, create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


class Base(DeclarativeBase):
    pass


class MovieModel(Base):
    __tablename__ = "movies"
    __table_args__ = (
        UniqueConstraint("title", "year", name="uq_movies_title_year"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)


class SeriesModel(Base):
    __tablename__ = "series"
    __table_args__ = (
        UniqueConstraint("title", "year", name="uq_series_title_year"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    seasons: Mapped[int] = mapped_column(Integer, nullable=False)
    episodes: Mapped[int] = mapped_column(Integer, nullable=False)


def create_engine_sqlite(db_path: str):
    """Cria o engine apontando para o arquivo SQLite."""
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    uri = f"sqlite:///{db_path}"
    return create_engine(uri, future=True)


def init_db(engine) -> None:
    """Inicializa as tabelas no banco."""
    Base.metadata.create_all(engine)


def insert_movie(engine, title: str, year: int, rating: float) -> bool:
    """Insere um filme. Retorna True se inseriu, False se já existe."""
    try:
        with Session(engine) as session:
            novo = MovieModel(title=title, year=year, rating=rating)
            session.add(novo)
            session.commit()
        return True
    except IntegrityError:
        return False


def insert_series(engine, title: str, year: int, seasons: int, episodes: int) -> bool:
    """Insere uma série. Retorna True se inseriu, False se for duplicada."""
    try:
        with Session(engine) as session:
            nova = SeriesModel(
                title=title,
                year=year,
                seasons=seasons,
                episodes=episodes,
            )
            session.add(nova)
            session.commit()
        return True
    except IntegrityError:
        return False

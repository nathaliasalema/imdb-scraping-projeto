#ex3 #ex4 #ex5
from __future__ import annotations

from dataclasses import dataclass


# ex3
@dataclass
class TV:
    title: str
    year: int

    def __str__(self) -> str:
        return f"{self.title} - {self.year}"
        

# ex4
@dataclass
class Movie(TV):
    rating: float

    def __str__(self) -> str:
        nota = f"{self.rating:.1f}"
        return f"{self.title} ({self.year}) | Nota {nota}"


# ex4
@dataclass
class Series(TV):
    seasons: int
    episodes: int

    def __str__(self) -> str:
        return f"{self.title} ({self.year}) | {self.seasons} temporadas, {self.episodes} episódios"

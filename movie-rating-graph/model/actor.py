"""Nel nodo Actor bisogna considerare anche l'età, controllando che sia valida"""
from dataclasses import dataclass

@dataclass
class Actor:
    id: str
    name: str
    height: int
    date_of_birth: str
    known_for_movies: str
    age: int # attributo richiesto aggiunto

    def __str__(self):
        return f"{self.name}"

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return isinstance(other, Actor) and self.id == other.id

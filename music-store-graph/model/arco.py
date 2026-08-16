"""Il DAO restituisce un oggetto Arco, anzichè una tupla, che impaccheta le informazioni"""
from dataclasses import dataclass
from model.artist import Artist

@dataclass
class Arco:
    artistA: Artist
    artistB: Artist
    peso: int

    def __str__(self):
        return f"{self.artistA} --> {self.artistB} : {self.peso}"

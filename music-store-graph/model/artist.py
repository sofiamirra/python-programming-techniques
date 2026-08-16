"""Oggetto di classe Artist per la creazione dei nodi"""
from dataclasses import dataclass

@dataclass
class Artist:
    ArtistId: int
    Name: str

    def __str__(self):
        return f"{self.Name}"

    def __hash__(self):
        return hash(self.ArtistId)

    def __eq__(self, other):
        return self.ArtistId == other.ArtistId

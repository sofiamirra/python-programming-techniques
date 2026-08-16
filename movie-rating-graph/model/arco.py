"""Il DAO restituisce un oggetto Arco, anzichè una tupla, che impaccheta le informazioni"""
from dataclasses import dataclass
from model.actor import Actor

@dataclass
class Arco:
    actorA: Actor
    actorB: Actor
    peso: int

    def __str__(self):
        return f"{self.actorA} --> {self.actorB} : {self.peso}"

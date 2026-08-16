from dataclasses import dataclass
from model.circuit import Circuit


@dataclass
class Arco:
    c1: Circuit
    c2: Circuit
    peso: int

    def __str__(self):
        return f"{self.c1} --> {self.c2} ({self.peso})"

from dataclasses import dataclass
from model.Constructor import Constructor

@dataclass
class Arco:
    c1: Constructor
    c2: Constructor
    peso: int

    def __str__(self):
        return (f"{self.c1} --> {self.c2} ({self.peso} piloti condivisi)")
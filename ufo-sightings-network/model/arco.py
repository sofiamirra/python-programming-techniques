from dataclasses import dataclass
from model.state import State


@dataclass
class Arco:
    s1: State
    s2: State
    peso: int

    def __str__(self):
        return f"{self.s1} <--> {self.s2} | peso={self.peso}"
from dataclasses import dataclass
from model.order import Order


@dataclass
class Arco:
    o1: Order
    o2: Order
    peso: int

    def __str__(self):
        return f"{self.o1} --> {self.o2} - Peso: {self.peso}"

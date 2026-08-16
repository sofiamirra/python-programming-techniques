from dataclasses import dataclass
from model.product import Product

@dataclass
class Arco:
    p1: Product
    p2: Product
    peso: int

    def __str__(self):
        return f"{self.p1} --> {self.p2} ({self.peso})"
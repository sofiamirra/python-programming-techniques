"""DTO per il trasporto delle informazioni sugli archi"""
from dataclasses import dataclass
from model.product import Product

@dataclass
class Arco:
    p1: Product
    p2: Product
    peso: int

# Non serve inserire inserire definizioni hashable e eq


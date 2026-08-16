"""Oggetto DTO per il trasporto dal DAO"""
from dataclasses import dataclass
from model.driver import Driver

@dataclass
class Arco:
    d1: Driver
    d2: Driver
    peso: int

    def __str__(self):
        return f"{self.d1} --> {self.d2} ({self.peso})"


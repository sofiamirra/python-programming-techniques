import decimal
import math
from dataclasses import dataclass


@dataclass
class State:
    id: str
    Name: str
    Capital: str
    Lat: float
    Lng: float
    Area: float
    Population: int
    Neighbors: []

    def __str__(self):
        return self.Name

    def __hash__(self):
        return hash(self.id)

    def distance_HV(self, other):
        """
        Function that calculate the approximate geodesic distance between two sightings.
        :param other: another sighting.
        :return: the approximate geodesic distance in kilometers
        """
        lat1 = self.Lat * math.pi / 180
        lon1 = self.Lng * math.pi / 180
        lat2 = other.Lat * math.pi / 180
        lon2 = other.Lng * math.pi / 180
        R = 6371  # earth radius in km
        a = math.sin(0.5 * (lat2 - lat1)) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(0.5 * (lon2 - lon1)) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return decimal.Decimal(R * c)

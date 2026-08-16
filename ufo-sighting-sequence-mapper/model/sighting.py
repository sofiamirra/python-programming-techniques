from dataclasses import dataclass
from datetime import datetime as dtime
import math


@dataclass
class Sighting:
    id: int
    datetime: dtime
    city: str
    state: str
    country: str
    shape: str
    duration: int
    duration_hm: str
    comments: str
    date_posted: dtime
    latitude: float
    longitude: float

    def __str__(self):
        return f"id:{self.id} - {self.city}  [{self.state}], {self.datetime.strftime("%Y-%m-%d %H:%M:%S")}"

    def __hash__(self):
        return hash(self.id)

    def distance_HV(self, other) -> float:
        """
        Function that calculate the approximate geodesic distance between two sightings.
        :param other: another sighting.
        :return: the approximate geodesic distance in kilometers
        """
        lat1 = self.latitude * math.pi / 180
        lon1 = self.longitude * math.pi / 180
        lat2 = other.latitude * math.pi / 180
        lon2 = other.longitude * math.pi / 180
        R = 6371  # earth radius in km
        a = math.sin(0.5 * (lat2 - lat1)) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(0.5 * (lon2 - lon1)) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c


from dataclasses import dataclass
from datetime import datetime as dtime

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

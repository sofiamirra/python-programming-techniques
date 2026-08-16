from dataclasses import dataclass


@dataclass
class State:
    _id: str
    _Name: str
    _Capital: str
    _Lat: float
    _Lng: float
    _Area: float
    _Population: int
    _Neighbors: []

    @property
    def id(self):
        return self._id

    @property
    def lat(self):
        return self._Lat

    @property
    def lng(self):
        return self._Lng

    @property
    def name(self):
        return self._Name

    def __str__(self):
        return self._Name

    def __hash__(self):
        return hash(self._id)
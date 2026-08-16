import datetime
from dataclasses import dataclass

@dataclass
class Driver:
    driverId: int
    driverRef: str
    number: int
    code: str
    forename: str
    surname: str
    dob: datetime.date
    nationality: str
    url: str

    def __hash__(self):
        return hash(self.driverId)

    def __eq__(self, other):
        return self.driverId == other.driverId

    def __str__(self):
        return self.driverRef


from dataclasses import dataclass
import datetime

@dataclass
class Constructor:
    constructorId: int
    constructorRef: str
    name: str
    nationality: str
    # data di nascita del pilota più anziano che abbia corso
    oldest_driver_dob: datetime.date = None

    def __hash__(self):
        return hash(self.constructorId)

    def __eq__(self, other):
        return self.constructorId == other.constructorId

    def __str__(self):
        return self.constructorRef

from dataclasses import dataclass, field

@dataclass
class Circuit:
    circuitId: int
    circuitRef: str
    name: str
    location: str
    country: str
    lat: float
    lng: float
    alt: int
    url: str
    racePlacements: dict = field(default_factory=dict)
    # dizionario le cui chiavi sono gli anni in cui il circuito ha ospitato la Formula1 (nel range selezionato)
    # e come valori una lista contenente i piazzamenti dei vari piloti nella gara considerata (anno, circuito)

    def __hash__(self):
        return hash(self.circuitId)

    def __eq__(self, other):
        return self.circuitId == other.circuitId

    def __str__(self):
        return self.circuitRef


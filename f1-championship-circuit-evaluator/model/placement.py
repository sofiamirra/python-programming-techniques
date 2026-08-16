from dataclasses import dataclass

@dataclass
class Placement:
    driverId: int
    time: int

    def __str__(self):
        return f"{self.driverId} ({self.time})"

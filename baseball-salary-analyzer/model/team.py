"""Oggetto Team che rappresenta i nodi del grafo"""
from dataclasses import dataclass

@dataclass
class Team:
    ID: int
    year: int
    teamCode: str
    divID: str
    div_ID: int
    teamRank: int
    games: int
    gamesHome: int
    wins: int
    losses: int
    divisionWinnner: str
    leagueWinner: str
    worldSeriesWinnner: str
    runs: int
    hits: int
    homeruns: int
    stolenBases: int
    hitsAllowed: int
    homerunsAllowed: int
    name: str
    park: str

    def __str__(self):
        return f"{self.name} ({self.teamCode})"

    def __hash__(self):
        return hash(self.ID)

    def __eq__(self, other):
        """Metodo per il confronto di due oggetti Team"""
        return self.ID == other.ID

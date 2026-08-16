import copy

import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._teams = []
        self._idMapTeams = None # inizializzo dizionario (ID: Team)
        self._bestPath = []
        self._bestScore = 0

    def getPath(self, v0):
        """Metodo GREEDY per cercare l'itinerario di peso massimo tra archi di peso decrescente,
            partendo dal nodo source, passando al più una volta per nodo"""
        self._bestPath = []
        self._bestScore = 0
        parziale = [v0] # il cammino parte dal nodo iniziale
       # listaVicini = self.getViciniOrdinati(parziale[-1])
       # parziale.append(listaVicini[0][0]) # nodo successivo con peso dell'arco maggiore
        self._ricorsione(parziale) # la ricorsione esplora tutti i cammini
        return self._bestPath, self._bestScore

    def _ricorsione(self, parziale):
        # CONDIZIONE OTTIMALITÀ e TERMINALE: verifico se parziale è una soluzione valida e, in caso, la salvo
        if self._getScore(parziale) > self._bestScore: # se è migliore di quella trovata, agggiorno
            self._bestPath = copy.deepcopy(parziale)
            self._bestScore = self._getScore(parziale)

        # ATTENZIONE! La condizione di termine e ottimalità sono unite
        # poichè la soluzione non deve avere un numero masssimo di nodi

        # CONDIZIONE RICORSIVA: espando parziale e faccio backtracking
        listaVicini = self.getViciniOrdinati(parziale[-1])
        for v in listaVicini: # ciclo sui vicini dell'ultimo nodo
            # RECALL: v[0] = nuovo vicino, v[1] = peso arco nuovo (da valori tupla)
            if v[0] not in parziale and (len(parziale) == 1 or self._grafo[parziale[-2]][parziale[-1]]['weight'] > v[1]):
                parziale.append(v[0])
                self._ricorsione(parziale) # proseguo la ricorsione sul nuovo cammino parziale
                parziale.pop()
                return # Siccome listaVicini era ordinata, v[0] era la miglior scelta possibile, quindi interrompo

    def _getScore(self, parziale):
        score = 0
        for i in range(0, len(parziale)-1):
            score += self._grafo[parziale[i]][parziale[i+1]]['weight']
        return score

    def creaGrafo(self, year):
        """Crea il grafo delle squadre ed assegna i pesi agli archi"""
        self._grafo.clear()
        self._grafo.add_nodes_from(self._teams) # aggiungo come nodi tutte le squadre dell'anno selezionato
        # Il grafo è COMPLETO, perciò esiste un arco tra ogni coppia di nodi
        for u in self._grafo.nodes(): # doppio ciclo sui nodi
            for v in self._grafo.nodes():
                if u != v: # se i due nodi sono diversi, aggiungo l'arco
                    self._grafo.add_edge(u, v)

        # Associo ogni oggetto Team al relativo ID (chiave) nel dizionario
        self._idMapTeams = {}
        for t in self._grafo.nodes():
            self._idMapTeams[t.ID] = t

        # Chiama il metodo dal DAO per recuperare il peso degli archi
        mapSalary = DAO.getSalariesTeam(year, self._idMapTeams)
        # assegna ad ogni arco la somma degli stipendi come peso
        for e in self._grafo.edges(): # e è una tupla contenente i due nodi di quell'arco
            self._grafo[e[0]][e[1]]["weight"] = mapSalary[e[0]] + mapSalary[e[1]]

    def getTeamsOfYear(self, year):
        """Recupera le squadre che hanno giocato in un certo anno"""
        self._teams = DAO.getTeamsOfYear(year)
        return self._teams

    def getAllYears(self):
        """Restituisce tutti gli anni disponibili"""
        return DAO.getAllYear()

    def getGraphDetails(self):
        """Restituisce il numero di nodi e archi del grafo"""
        return len(self._grafo.nodes()), len(self._grafo.edges())

    def getViciniOrdinati(self, source):
        """Ritorna i vicini di source ordinati per peso dell'arco collegante"""
        vicini = self._grafo.neighbors(source)  # recupera i vicini del nodo sorgente
        viciniTupla = []  # devo inserirli in una struttura per recuperare il peso
        for v in vicini:  # inserisco gli elementi in una lista di tuple (team_vicini, peso_arco)
            viciniTupla.append((v, self._grafo[source][v]['weight']))
        viciniTupla.sort(key=lambda x: x[1], reverse=True) # ordino per peso decrescente
        return viciniTupla


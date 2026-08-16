import copy

from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMapSights = {}
        self._lista_archi = []

    def getShapes(self):
        return DAO.getAllShapes()

    def getValues(self):
        return DAO.getBorderValues()

    def buildGraph(self, shape, lat, lng):
        self._graph.clear()
        self._lista_archi.clear()
        self._idMapSights = {}
        nodes = DAO.getAllNodes(shape, lat, lng)
        self._graph.add_nodes_from(nodes)
        for s in nodes:
            self._idMapSights[s.id] = s
        allEdges = DAO.getAllEdges(shape, lat, lng, self._idMapSights)
        for e in allEdges:
            self._graph.add_edge(e.s1, e.s2, weight=e.peso)
            self._lista_archi.append(e)

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getTop5Archi(self):
        self._lista_archi.sort(key=lambda x: x.peso, reverse=True)
        return self._lista_archi[:5]

    def getTop5Nodi(self):
        nodes = list(self._graph.nodes)
        nodi_ordinati = sorted(nodes, key=lambda n: self._graph.degree(n), reverse=True)
        return nodi_ordinati[:5]

    # ============================================================
    # MODEL - RICORSIONE PER PERCORSO CON DENSITÀ CRESCENTE
    # ============================================================

    def getPercorso(self):
        self._bestPath = []
        self._bestScore = -float("inf")

        if len(self._graph.nodes) == 0:
            return [], 0

        for n in self._graph.nodes:
            parziale = [n]
            self._ricorsione(parziale)

        if len(self._bestPath) == 0:
            return [], 0

        return self._bestPath, self._bestScore

    def _ricorsione(self, parziale):
        if len(parziale) > 1:
            score = self._getScore(parziale)

            if score > self._bestScore:
                self._bestPath = copy.deepcopy(parziale)
                self._bestScore = score

        for n in self._graph.neighbors(parziale[-1]):
            if n not in parziale:
                densita_corrente = self.getDensita(parziale[-1])
                densita_nuova = self.getDensita(n)

                if densita_nuova > densita_corrente:
                    parziale.append(n)
                    self._ricorsione(parziale)
                    parziale.pop()

    def _getScore(self, parziale):
        peso_totale = 0
        distanza_totale = 0

        for i in range(0, len(parziale) - 1):
            n1 = parziale[i]
            n2 = parziale[i + 1]

            peso_totale += self._graph[n1][n2]["weight"]
            distanza_totale += n1.distance_HV(n2)

        if distanza_totale == 0:
            return 0

        return peso_totale / distanza_totale

    def getDensita(self, stato):
        if stato.Area == 0:
            return 0

        return stato.Population / stato.Area

    def getPathDetails(self, path):
        dettagli = []

        if path is None or len(path) < 2:
            return dettagli

        for i in range(0, len(path) - 1):
            n1 = path[i]
            n2 = path[i + 1]

            peso = self._graph[n1][n2]["weight"]
            distanza = n1.distance_HV(n2)

            dettagli.append((n1, n2, peso, distanza))

        return dettagli


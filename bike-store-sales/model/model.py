import copy

import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._idMapProducts = {}
        self._products = []

    def getDateRange(self):
        return DAO.getDateRange()

    def getCategories(self):
        """Per passare il metodo al Controller"""
        return DAO.getCategorie()

    def getAllNodes(self):
        return self._graph.nodes

    def buildGraph(self, categories, date1, date2):
        self._graph.clear()
        self._products = DAO.getProductsByCategory(categories)
        for p in self._products:
            self._idMapProducts[p.product_id] = p
        self._graph.add_nodes_from(self._products)
        allEdges = DAO.getAllEdges(categories, date1, date2, self._idMapProducts)
        for e in allEdges:
            self._graph.add_edge(e.p1, e.p2, weight=e.peso)

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getBestSellers(self):
        listBestSellers = []
        for n in self._graph.nodes:
            score = 0
            for e in self._graph.out_edges(n, data=True):
                score += e[2]["weight"]
            for e in self._graph.in_edges(n, data=True):
                score -= e[2]["weight"]
            listBestSellers.append((n, score))
            listBestSellers.sort(key=lambda x:x[1], reverse=True)
        return listBestSellers[0:5]

    def getBestPath(self, t, v0, vf):
        # Lunghezza definita, nodo di partenza, nodo di arrivo
        self._bestPath = []
        self._bestScore = 0
        parziale = [v0] # preparo il cammino dal nodo di partenza
        self._ricorsione(parziale, t, v0, vf) # passo tutti i vincoli
        return self._bestPath, self._bestScore

    def _ricorsione(self, parziale, t, v0, vf):
        # CONDIZIONE OTTIMALITÀ E TERMINAZIONE
        if len(parziale) == t: # riferita al numero di archi
            # Se sono lungo 't', controllo: sono arrivato a destinazione?
            # E il mio punteggio ha battuto il record storico?
            if parziale[-1] == vf and self._getScore(parziale) > self._bestScore:
                self._bestPath = copy.deepcopy(parziale)
                self._bestScore = self._getScore(parziale)
            return

        # Uso successors() per rispettare il verso degli archi!
        for n in self._graph.successors(parziale[-1]):
            if n not in parziale: # Il nodo non deve essere già nel cammino
                parziale.append(n)
                self._ricorsione(parziale, t, v0, vf) # continuo l'esplorazione
                parziale.pop()

    def _getScore(self, parziale):
        score = 0
        # Ciclo da 0 fino al penultimo elemento
        for i in range(0, len(parziale)-1):
            # Sommo il peso dell'arco tra il nodo i e il nodo successivo i+1
            score += self._graph[parziale[i]][parziale[i+1]]["weight"]
        return score
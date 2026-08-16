import copy

import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._idMapProducts = {}

    def getDateRange(self):
        return DAO.getDateRange()

    def getCategories(self):
        return DAO.getCategorie()

    def getNodes(self, idCategory):
        return DAO.getAllNodes(idCategory)

    def buildGraph(self, categoryId, date1, date2):
        self._graph.clear()
        self._idMapProducts = {}
        nodes = DAO.getAllNodes(categoryId)
        self._graph.add_nodes_from(nodes)
        for p in nodes:
            self._idMapProducts[p.product_id] = p

        allEdges = DAO.getAllEdges(date1, date2, categoryId, self._idMapProducts)
        for e in allEdges:
            self._graph.add_edge(e.p2, e.p1, weight=e.peso)

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getBestSellers(self):
        listBestSellers = []
        for n in self._graph.nodes:
            uscenti = self._graph.out_degree(n, weight='weight')
            entranti = self._graph.in_degree(n, weight='weight')
            score = entranti - uscenti
            listBestSellers.append((n, score))

        listBestSellers.sort(key=lambda x: x[1], reverse=True)
        return listBestSellers[0:5]

    def getPercorso(self, sourceStr, targetStr, k):
        self._bestPath = []
        self._bestScore = -float("inf")
        self._target = None
        self._k = k

        if sourceStr is None or targetStr is None:
            return [], 0

        if k <= 0:
            return [], 0

        try:
            sourceId = int(sourceStr)
            targetId = int(targetStr)
        except ValueError:
            return [], 0

        source = self._idMapProducts.get(sourceId)
        target = self._idMapProducts.get(targetId)

        if source is None or target is None:
            return [], 0

        if source not in self._graph.nodes or target not in self._graph.nodes:
            return [], 0

        self._target = target

        parziale = [source]
        self._ricorsione(parziale)

        if len(self._bestPath) == 0:
            return [], 0

        return self._bestPath, self._bestScore

    def _ricorsione(self, parziale):
        # Se ho superato la lunghezza richiesta, ramo inutile.
        if len(parziale) > self._k:
            return

        # Se sono arrivata al target, posso accettare il cammino solo se ha lunghezza esatta K.
        # Se sono arrivata al target troppo presto, mi fermo comunque.
        if parziale[-1] == self._target:
            if len(parziale) == self._k:
                score = self._getScore(parziale)

                if score > self._bestScore:
                    self._bestPath = copy.deepcopy(parziale)
                    self._bestScore = score

            return

        # Se ho raggiunto lunghezza K ma non sono sul target, il cammino non è valido.
        if len(parziale) == self._k:
            return

        # Grafo diretto: uso successors per rispettare il verso degli archi.
        for n in self._graph.successors(parziale[-1]):
            if n not in parziale:
                parziale.append(n)
                self._ricorsione(parziale)
                parziale.pop()

    def _getScore(self, parziale):
        score = 0

        for i in range(0, len(parziale) - 1):
            score += self._graph[parziale[i]][parziale[i + 1]]["weight"]

        return score
import copy
import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._idMapOrders = {}
        self._lista_archi = []

    def getStore(self):
        return DAO.getAllStores()

    def getAllNodes(self, storeId):
        return DAO.getAllNodes(storeId)

    def buildGraph(self, storeId, k):
        self._graph.clear()
        self._lista_archi.clear()
        self._idMapOrders = {}
        nodes = DAO.getAllNodes(storeId)
        self._graph.add_nodes_from(nodes)
        for o in nodes:
            self._idMapOrders[o.order_id] = o
        allEdges = DAO.getAllEdges(storeId, self._idMapOrders, k)
        for e in allEdges:
            self._graph.add_edge(e.o1, e.o2, weight=e.peso)
            self._lista_archi.append(e)

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getTop5Archi(self):
        self._lista_archi.sort(key=lambda x: x.peso, reverse=True)
        return self._lista_archi[:5]

    def getCammino(self, sourceStr):
        # sourceStr arriva dal Dropdown come stringa, quindi lo converto in int
        source = self._idMapOrders[int(sourceStr)]

        lp = []

        # Creo l'albero DFS partendo dal nodo sorgente
        tree = nx.dfs_tree(self._graph, source)

        # Prendo tutti i nodi raggiunti dalla DFS
        nodi = list(tree.nodes())

        # Per ogni nodo raggiunto ricostruisco il cammino source -> node
        for node in nodi:
            tmp = [node]

            while tmp[0] != source:
                pred = nx.predecessor(tree, source, tmp[0])
                tmp.insert(0, pred[0])

            # Tengo il cammino più lungo trovato nell'albero DFS
            if len(tmp) > len(lp):
                lp = copy.deepcopy(tmp)

        return lp

    def getPercorsoDecrescentePesoMassimo(self, source):
        self._bestPath = []
        self._bestScore = 0

        parziale = [source]
        self._ricorsioneDecrescente(parziale)

        return self._bestPath, self._bestScore

    def _ricorsioneDecrescente(self, parziale):
        score = self._getScore(parziale)

        if score > self._bestScore:
            self._bestPath = copy.deepcopy(parziale)
            self._bestScore = score

        for n in self._graph.neighbors(parziale[-1]):
            if n not in parziale:
                peso_corrente = self._graph[parziale[-1]][n]['weight']

                if len(parziale) == 1:
                    peso_precedente = float('inf')
                else:
                    peso_precedente = self._graph[parziale[-2]][parziale[-1]]['weight']

                if peso_corrente < peso_precedente:
                    parziale.append(n)
                    self._ricorsioneDecrescente(parziale)
                    parziale.pop()

    def _getScore(self, parziale):
        score = 0
        for i in range(0, len(parziale) - 1):
            score += self._graph[parziale[i]][parziale[i + 1]]['weight']
        return score





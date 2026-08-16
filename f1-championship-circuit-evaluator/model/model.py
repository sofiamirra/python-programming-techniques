import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMapCircuits = {}

    def getYears(self):
        return DAO.getAllYears()

    def buildGraph(self, y1, y2):
        self._graph.clear()
        self._idMapCircuits = {}
        nodes = DAO.getAllCircuits()
        self._graph.add_nodes_from(nodes)
        for c in nodes:
            self._idMapCircuits[c.circuitId] = c

        allEdges = DAO.getAllEdges(y1, y2, self._idMapCircuits)
        for e in allEdges:
            self._graph.add_edge(e.c1, e.c2, weight=e.peso)

        for c in self._graph.nodes:
            # Cicla solo sugli anni interni al range (estremi esclusi)
            for anno in range(y1 + 1, y2):
                # Recupera i piazzamenti per quell'anno specifico
                placements = DAO.getPlacements(anno, c.circuitId)

                # Se la lista non è vuota (ovvero si è corso in quell'anno), aggiungila al dizionario
                if len(placements) > 0:
                    c.racePlacements[anno] = placements

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getComponentiConnesseDetails(self):
        componenti = list(nx.connected_components(self._graph))
        largest = max(componenti, key=len)
        min_weights = {}
        for node in self._graph.nodes:
            edges = self._graph.edges(node, data=True)
            if edges:
                # Calcoliamo il minimo tra tutti gli archi incidenti
                min_weights[node] = min(e[2]['weight'] for e in edges)
            else:
                # Caso nodo senza archi
                min_weights[node] = 0

        # 3. Ordina la lista usando il dizionario come riferimento
        # Usiamo .get(n, 0) per sicurezza, nel caso un nodo non fosse nel dizionario
        nodi_ordinati = sorted(list(largest), key=lambda n: min_weights.get(n, 0), reverse=True)

        return largest, nodi_ordinati, min_weights




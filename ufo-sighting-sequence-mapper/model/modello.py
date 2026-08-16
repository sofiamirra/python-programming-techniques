from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._sightings = []
        self._idMapSights = {}

    def getAllYears(self):
        return DAO.getAllYears()

    def getAllStates(self, year):
        return DAO.get_all_states(year)

    def buildGraph(self, year, state):
        self._graph.clear()
        self._idMapSights = {}
        nodes = DAO.getAllNodes(year, state)
        self._graph.add_nodes_from(nodes)
        for s in nodes:
            self._idMapSights[s.id] = s
        self.add_edges(year, state)

    def add_edges(self, year, state):
        """Recupera le coppie con stessa forma dal DAO e calcola la distanza"""

        # Il DAO esegue la query e ci restituisce una lista di dizionari
        coppie_grezze = DAO.getEdgesInformation(year, state)

        # Analizziamo una per una le coppie "candidate" trovate dal database
        for riga in coppie_grezze:
            # Estraiamo i semplici numerini (ID) dal dizionario restituito da SQL
            id_1 = riga['id1']
            id_2 = riga['id2']

            # Usiamo self._idMapSights (che abbiamo riempito prima) per "tradurre" l'ID nell'oggetto completo.
            s1 = self._idMapSights.get(id_1)
            s2 = self._idMapSights.get(id_2)

            # Procediamo solo se la "traduzione" è andata a buon fine per entrambi i nodi.
            if s1 is not None and s2 is not None:
                # Python legge in automatico latitudine e longitudine e calcola
                distanza = s1.distance_HV(s2)

                # Filtro sulla distanza
                if distanza < 100:
                    # Aggiungiamo finalmente la connessione al nostro grafo.
                    self._graph.add_edge(s1, s2)

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getComponentiConnesse(self):
        componenti = list(nx.connected_components(self._graph))
        largest = max(componenti, key=len)
        nodi = sorted(largest, key=lambda n:self._graph.degree(n), reverse=True)

        return len(componenti), largest, nodi

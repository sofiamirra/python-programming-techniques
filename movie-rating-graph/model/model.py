import networkx as nx
from database.DAO import DAO
from model.arco import Arco

class Model:
    def __init__(self):
        self._graph = nx.Graph() # grafo PESATO ma non ORIENTATO
        self._actors = DAO.getAllActors()
        self._idMapActors = {} # dizionario per mappare gli attori
        for a in self._actors:
            self._idMapActors[a.id] = a
        self._lista_archi = []  # Lista per salvare i nostri oggetti Arco

    def buildGraph(self, r1, r2):
        """Metodo per la creazione del grafo"""
        self._graph.clear()
        # Aggiunge i nodi già filtrati dal DAO (attori validi)
        nodes = DAO.getAllNodes(r1, r2, self._idMapActors)
        self._graph.add_nodes_from(nodes)
        # Aggiungo gli archi tra attori con film in comune
        self._addEdges(r1, r2)

    def _addEdges(self, r1, r2):
        """Recupera dal DAO le coppie di attori e popola gli archi del grafo"""
        coppie_grezze = DAO.getCoppieAttori(r1, r2)
        self._lista_archi.clear()

        for id_1, id_2, peso in coppie_grezze:
            # Recupero oggetti Actor dalla mappa
            nodo_1 = self._idMapActors.get(id_1)
            nodo_2 = self._idMapActors.get(id_2)

            # Se i nodi non esistono, salto
            if nodo_1 is None or nodo_2 is None:
                continue

            # Aggiungo l'arco solo se entrambi gli attori sono nel grafo
            # (filtro per rating e attori validi)
            if nodo_1 not in self._graph.nodes or nodo_2 not in self._graph.nodes:
                continue

            # Creo l'oggetto Arco per stampare la top 5
            arco_nuovo = Arco(nodo_1, nodo_2, peso)
            self._lista_archi.append(arco_nuovo)
            # Aggiungo l'arco al grafo pesato
            self._graph.add_edge(nodo_1, nodo_2, weight=int(peso))

    def getAllRatings(self):
        """Restituisce tutti i ratings disponibili"""
        return DAO.getAllRatings()

    def getGraphDetails(self):
        """Restituisce numero di vertici e archi con informazioni per la View"""
        return len(self._graph.nodes), len(self._graph.edges)

    def getTop5Archi(self):
        """Restituisce i 5 archi con peso maggiore in ordine decrescente"""
        self._lista_archi.sort(key=lambda x: x.peso, reverse=True)
        return self._lista_archi[:5]

    def getComponentiConnesseDetails(self):
        """Restituisce il numero di componenti connesse e la componente più grande"""
        # (gruppi di nodi in cui ogni nodo è raggiungibile da altri attraverso archi)

        # Conta quante "isole separate" ci sono nel grafo (A -- B -- C), (D -- F)
        n_componenti = nx.number_connected_components(self._graph)

        # Restituisce tutte le componenti, ogni componente è un insieme di nodi
        componenti = nx.connected_components(self._graph)

        # Prende la componente con più nodi
        componente_piu_grande = max(componenti, key=len)
        return n_componenti, componente_piu_grande



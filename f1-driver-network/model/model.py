import copy

import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        # inizializzazione della struttura del grafo vuota
        self._graph = nx.Graph()
        self._drivers = []
        self._idMapDrivers = {}
        self._lista_archi = []

    def getAllYears(self):
        """Metodo per chiamare gli anni dal DAO"""
        return DAO.getAllYears()

    def buildGraph(self, y1, y2):
        """Costruzione del grafo"""
        self._graph.clear()
        self._idMapDrivers = {}
        nodes = DAO.getAllNodes(y1, y2) # recupero dei soli nodi che soddisfano i requisiti
        self._graph.add_nodes_from(nodes)
        for d in nodes:
            # la chiave deve sempre corrispondere all'attributo chiave primaria
            self._idMapDrivers[d.driverId] = d

        # caricamento degli archi tramite il DAO
        allEdges = DAO.getAllEdges(y1, y2, self._idMapDrivers)
        for e in allEdges:
            self._graph.add_edge(e.d1, e.d2, weight=e.peso)
            self._lista_archi.append(e)

    def getGraphDetails(self):
        """Restituisce il conteggio attuale dei nodi e degli archi per la verifica immediata"""
        return len(self._graph.nodes), len(self._graph.edges)

    def getTop3Archi(self):
        """Restituisce i 3 archi con peso maggiore in ordine decrescente"""
        self._lista_archi.sort(key=lambda x: x.peso, reverse=True)
        return self._lista_archi[:3]

    def getComponentiConnesseDetails(self):
        # Conta quante "isole separate" ci sono nel grafo (A -- B -- C), (D -- F)
        # restituisce tutte le componenti, ogni componente è un insieme di nodi
        componenti = list(nx.connected_components(self._graph))

        # Prende la componente con più nodi
        largest = max(componenti, key=len)
        nodi_ordinati = sorted(largest, key=lambda n: self._graph.degree(n), reverse=True)

        return len(componenti), largest, nodi_ordinati

    def getListaPilotiOttima(self, k):
        """Prepara le variabili globali, calcola le componenti connesse e innesca la ricorsione"""
        self._optListPiloti = []
        self._optMinDistGiorni = float('inf') # inizializzo il minimo a un valore altissimo

        components = list(nx.connected_components(self._graph)) # lista di tutte le componenti connesse
        if len(components) < k: # se non ho abbastanza componenti connesse da cui pescare è impossibile
            return None, None

        parziale = []
        # innesco la ricorsione partendo dalla prima componente connessa
        self._ricorsione(components, k, parziale, 0)
        return self._optListPiloti, self._optMinDistGiorni

    def _ricorsione(self, components, k, parziale, indexComponent):
        """Esplora le combinazioni scegliendo se pescare o meno un pilota dalla componente corrente"""
        # CONDIZIONE DI OTTIMALITÀ:
        if len(parziale) == k:
            # estraggo le date di nascita e trovo la differenza tra il piu giovane e il piu vecchio
            dateDiNascita = [p.dob for p in parziale]
            diff = (max(dateDiNascita) - min(dateDiNascita)).days
            # se la differenza in giorni e minore del mio record attuale aggiorno la soluzione migliore
            if diff < self._optMinDistGiorni:
                self._optListPiloti = copy.deepcopy(parziale)
                self._optMinDistGiorni = diff
            return # mi fermo perche ho raggiunto la lunghezza richiesta

        # CONDIZIONE DI TERMINAZIONE:
        # 1) Sono arrivato oltre l'ultima scatola disponibile
        # 2) Le scatole rimanenti sono meno dei piloti che mi mancano per arrivare a k
        comp_rimanenti = len(components) - indexComponent
        piloti_mancanti = k - len(parziale)
        if indexComponent >= len(components) or comp_rimanenti < piloti_mancanti:
            return

        # Caso 1: decido di pescare un pilota da questa componente
        componente = components[indexComponent]
        for pilota in componente:
            parziale.append(pilota)
            self._ricorsione(components, k, parziale, indexComponent + 1)
            parziale.pop()

        # Caso 2: decido di non prendere nessun pilota da questa componente
        # vado avanti esplorando la scatola successiva mantenendo il parziale intatto
        self._ricorsione(components, k, parziale, indexComponent + 1)
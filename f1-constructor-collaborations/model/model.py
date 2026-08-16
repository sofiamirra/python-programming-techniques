import copy

import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._constructors = []
        self._idMapConstructors = {}
        self._lista_archi = []

    def getYears(self):
        return DAO.getAllYears()

    def buildGraph(self, year1, year2):
        self._graph.clear()
        self._idMapConstructors = {}
        nodes = DAO.getConstructors(year1, year2)
        self._graph.add_nodes_from(nodes)
        for c in nodes:
            self._idMapConstructors[c.constructorId] = c
        allEdges = DAO.getAllEdges(year1, year2, self._idMapConstructors)
        for e in allEdges:
            self._graph.add_edge(e.c1, e.c2, weight=e.peso)
            self._lista_archi.append(e)

        # aggiorniamo il campo oldest_driver_dob
        for squadra in self._graph.nodes:
            DAO.getDoB(squadra, year1, year2)

    def getGraphDetails(self):
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

    def getListaSquadreOttima(self, k):
        """Prepara le variabili globali, calcola le componenti connesse e innesca la ricorsione"""
        self._optListSquadre = []
        self._optMinDistGiorni = float('inf') # inizializzo il minimo a un valore altissimo

        components = list(nx.connected_components(self._graph)) # lista di tutte le componenti connesse
        if len(components) < k: # se non ho abbastanza componenti connesse da cui pescare è impossibile
            return None, None

        parziale = []
        # innesco la ricorsione partendo dalla prima componente connessa
        self._ricorsione(components, k, parziale, 0)
        return self._optListSquadre, self._optMinDistGiorni

    def _ricorsione(self, components, k, parziale, indexComponent):
        """Esplora le combinazioni scegliendo se pescare o meno una squadra dalla componente corrente"""
        # CONDIZIONE DI OTTIMALITÀ:
        if len(parziale) == k:
            # estraggo le date di nascita e trovo la differenza tra il piu giovane e il piu vecchio
            dateDiNascita = [s.oldest_driver_dob for s in parziale]
            diff = (max(dateDiNascita) - min(dateDiNascita)).days
            # se la differenza in giorni e minore del mio record attuale aggiorno la soluzione migliore
            if diff < self._optMinDistGiorni:
                self._optListSquadre = copy.deepcopy(parziale)
                self._optMinDistGiorni = diff
            return # mi fermo perche ho raggiunto la lunghezza richiesta

        # CONDIZIONE DI TERMINAZIONE:
        # 1) Sono arrivato oltre l'ultima scatola disponibile
        # 2) Le scatole rimanenti sono meno delle squadre che mi mancano per arrivare a k
        comp_rimanenti = len(components) - indexComponent
        squadre_mancanti = k - len(parziale)
        if indexComponent >= len(components) or comp_rimanenti < squadre_mancanti:
            return

        # Caso 1: decido di pescare un pilota da questa componente
        componente = components[indexComponent]
        for squadra in componente:
            # La squadra entra nel parziale SOLO se la sua data non è None
            if squadra.oldest_driver_dob is not None:
                parziale.append(squadra)
                self._ricorsione(components, k, parziale, indexComponent + 1)
                parziale.pop()

        # Caso 2: decido di non prendere nessun pilota da questa componente
        # vado avanti esplorando la scatola successiva mantenendo il parziale intatto
        self._ricorsione(components, k, parziale, indexComponent + 1)




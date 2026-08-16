import copy
import networkx as nx
from database.DAO import DAO

class Model:
    def __init__(self):
        self._graph = nx.Graph() # inizializzazione grafo
        # Carichiamo tutti gli Aeroporti per mapparli nel dizionario
        self._airports = DAO.getAllAirports()
        self._idMapAirports = {}
        for a in self._airports:
            self._idMapAirports[a.ID] = a
        self._bestCammino = []
        self._bestScore = 0

    def getCamminoOttimo(self, v0, v1, t):
        """Metodo per cercare l'itinerario che massimizzi il numero totale di voli,
            ovvero che massimizza la somma dei pesi degli archi attraversati"""
        self._bestCammino = []
        self._bestScore = 0
        parziale = [v0] # il cammino parte dall'aeroporto iniziale
        self._ricorsione(parziale, v1, t) # la ricorsione esplora tutti i cammini fino a t tratte
        return self._bestCammino, self._bestScore

    def _ricorsione(self, parziale, v1, t):
        # CONDIZIONE OTTIMALITÀ: verifico se parziale è una soluzione valida e, in caso, la salvo
        if parziale[-1] == v1: # potenziale soluzione ottima, verifico
            if self._getScore(parziale) > self._bestScore: # se è migliore di quella trovata, agggiorno
                self._bestCammino = copy.deepcopy(parziale)
                self._bestScore = self._getScore(parziale)

        # CONDIZIONE TERMINALE: verifico se ha senso aggiungere elementi in parziale, oppure esco
        if len(parziale) == t+1: # parziale ha raggiunto il numero massimo di tratte
            return # non ha senso aggiungere altri archi

        # ATTENZIONE! La condizione di termine e ottimalità sono controlli separati
        # poichè la soluzione può anche essere più corta di t

        # CONDIZIONE RICORSIVA: espando parziale e faccio backtracking
        for n in self._graph.neighbors(parziale[-1]): # ciclo sui vicini dell'ultimo nodo
            if n not in parziale: # verifico che non sia già stato aggiunto
                parziale.append(n)
                self._ricorsione(parziale, v1, t) # proseguo la ricorsione sul nuovo cammino parziale
                parziale.pop()

    def _getScore(self, parziale):
        sumPesi = 0
        for i in range(0, len(parziale)-1):
            sumPesi += self._graph[parziale[i]][parziale[i+1]]['weight']
        return sumPesi

    def buildGraph(self, nMin):
        """Metodo per la creazione del grafico"""
        self._graph.clear() # reset per analisi multiple
        # 1. Aggiunge i Nodi (filtrati dal DAO)
        nodes = DAO.getAllNodes(nMin, self._idMapAirports)
        self._graph.add_nodes_from(nodes)
        # 2. Aggiunge gli Archi
        self._addEdges()

    def _addEdges(self):
        """Recupera le rotte e popola gli archi del grafo"""
        allTratte = DAO.getAllEdges(self._idMapAirports)
        # Le tratte hanno due problemi:
        # i) il grafo è "non orientato", perciò bisogna sommare tutte le tratte
        # (Milano --> Roma = Roma --> Milano)
        # ii) gli archi devono essere compresi tra gli aeroporti filtrati

        for t in allTratte:
            # Mi assicuro che l'aeroporto di partenza e destinazione siano tra quelli
            # con almeno N compagnie di volo (ovvero nodi del grafo)
            if t.aeroportoP in self._graph and t.aeroportoA in self._graph:
                # Se l'arco (Milano --> Roma o Roma --> Milano) è già stato aggiunto
                if self._graph.has_edge(t.aeroportoP, t.aeroportoA):
                    # incrementa il peso dell'arco in questione
                    self._graph[t.aeroportoP][t.aeroportoA]['weight'] += t.peso
                # Altrimenti, creo l'arco nuovo e gli assegno il peso
                else:
                    self._graph.add_edge(t.aeroportoP, t.aeroportoA, weight=t.peso)

    def getViciniOrdinati(self, source):
        """Ritorna i vicini di source ordinati per peso dell'arco collegante (bottone Aeroporti Connessi)"""
        vicini = self._graph.neighbors(source) # recupera i vicini del nodo sorgente
        viciniTupla = [] # devo inserirli in una struttura per recuperare il peso
        for v in vicini: # inserisco gli elementi in una lista di tuple (aeroporto_vicino, peso_arco)
            viciniTupla.append( (v, self._graph[source][v]['weight']) )
        viciniTupla.sort(key=lambda x: x[1], reverse=True) # ordino per peso decrescente
        return viciniTupla

    def hasPath(self, v0, v1):
        """"Restituisce True se qualche cammino tra v0 e v1 esiste, altrimenti restituisce False"""
        return v1 in nx.node_connected_component(self._graph, v0)

    def getPath(self, v0, v1):
        """Esplorazione del grafo tramite Dijkstra per ottenere un cammino VALIDO tra i nodi (bottone Test Connessione)"""
        # Non è esplicitato il metodo di ricerca (BFS, DFS o Dijkstra), ma è solo chiesto un cammino valido
        path = nx.dijkstra_path(self._graph, v0, v1) # trova cammino di costo minimo rispetto ai pesi degli archi
        return path

    def getGraphDetails(self):
        """Restituisce le tuple per la View"""
        # Restituiamo una tupla con il numero totale di nodi e archi
        return len(self._graph.nodes), len(self._graph.edges)

    def getAllNodes(self):
        """Restituisce i nodi del grafo ordinati per IATA_CODE (per il menù a tendina)"""
        nodes = list(self._graph.nodes)
        nodes.sort(key=lambda x: x.IATA_CODE)
        return nodes

import copy

import networkx as nx
from database.DAO import DAO
from model.arco import Arco


class Model:
    def __init__(self):
        self._graph = nx.DiGraph() # grafo orientato e pesato
        # Carichiamo tutti gli artisti per mapparli nel dizionario
        self._artists = DAO.getAllArtists()
        self._idMapArtists = {}
        for artist in self._artists:
            self._idMapArtists[artist.ArtistId] = artist
        self._lista_archi = []  # Lista per salvare i nostri oggetti Arco

    def getPath(self, v0):
        """Metodo per cercare l'itinerario che massimizzi il numero totale di nodi con archi in sequenza crescente"""
        self._bestPath = []
        self._bestScore = 0
        parziale = [v0] # il cammino parte dal nodo iniziale
        self._ricorsione(parziale) # la ricorsione esplora tutti i cammini
        return self._bestPath, self._bestScore

    def _ricorsione(self, parziale):
        # CONDIZIONE OTTIMALITÀ e TERMINALE: verifico se parziale è una soluzione valida e, in caso, la salvo
        if len(parziale) > self._bestScore: # se è migliore di quella trovata, agggiorno
            self._bestPath = copy.deepcopy(parziale)
            self._bestScore = len(parziale)

        # ATTENZIONE! La condizione di termine e ottimalità sono unite
        # poichè la soluzione non deve avere un numero masssimo di nodi

        # CONDIZIONE RICORSIVA: espando parziale e faccio backtracking
        for n in self._graph.successors(parziale[-1]):  # ciclo sui vicini dell'ultimo nodo
            if n not in parziale: # verifico che non sia già stato aggiunto (grafo semplice)
                peso_corrente = self._graph[parziale[-1]][n]['weight'] # peso dell'arco che sto per attraversare
                if len(parziale) == 1:
                    # Al primo salto non c'è un arco precedente, quindi simulo un peso minimo
                    peso_precedente = -1
                else:
                    peso_precedente = self._graph[parziale[-2]][parziale[-1]]['weight'] # peso tra il penultimo e l'ultimo nodo
                if peso_corrente > peso_precedente:
                    parziale.append(n)
                    self._ricorsione(parziale)  # proseguo la ricorsione sul nuovo cammino parziale
                    parziale.pop()

    def buildGraph(self, genre_id):
        """Metodo per la creazione del grafo"""
        self._graph.clear()
        self._lista_archi.clear()  # Svuoto la lista a ogni nuova creazione

        # 1. Aggiungiamo i nodi filtrati
        nodes = DAO.getAllNodes(genre_id, self._idMapArtists)
        self._graph.add_nodes_from(nodes)

        # 2. Recupero le informazioni dal DB
        mappa_popolarita = DAO.getMappaPopolarita(genre_id)
        coppie_grezze = DAO.getCoppieArtisti(genre_id)

        # 3. Trasformo le coppie grezze in oggetti Arco
        for id_1, id_2 in coppie_grezze:
            nodo_1 = self._idMapArtists.get(id_1)
            nodo_2 = self._idMapArtists.get(id_2)

            # Se il nodo non è nel grafo, lo salto
            if nodo_1 not in self._graph.nodes or nodo_2 not in self._graph.nodes:
                continue

            # Leggo la popolarità. Uso .get() per avere 0 se l'artista non ha vendite
            pop_1 = mappa_popolarita.get(id_1, 0)
            pop_2 = mappa_popolarita.get(id_2, 0)

            # Il peso dell'arco è la somma delle rispettive popolarità
            peso_totale = pop_1 + pop_2

            # Recupero i veri oggetti Artist dalla mappa
            nodo_1 = self._idMapArtists[id_1]
            nodo_2 = self._idMapArtists[id_2]

            # con verso da A a B se la popolarità di A è maggiore
            if pop_1 > pop_2:
                self._lista_archi.append(Arco(nodo_1, nodo_2, peso_totale))
            # con verso da B a A se la popolarità di B è maggiore
            elif pop_2 > pop_1:
                self._lista_archi.append(Arco(nodo_2, nodo_1, peso_totale))
            # Se A e B hanno la stessa popolarità, aggiungere due archi in entrambi i versi.
            else:
                self._lista_archi.append(Arco(nodo_1, nodo_2, peso_totale))
                self._lista_archi.append(Arco(nodo_2, nodo_1, peso_totale))

        # 4. Inserisco gli archi nel grafo leggendoli dalla lista
        for a in self._lista_archi:
            self._graph.add_edge(a.artistA, a.artistB, weight=a.peso)

    def getAllGenres(self):
        """Restituisce tutti i generi musicali disponibili"""
        return DAO.getAllGenres()

    def getGraphDetails(self):
        """Restituisce numero di vertici e archi con informazioni per la View"""
        return len(self._graph.nodes), len(self._graph.edges)

    def getAllNodes(self):
        """Restituisce i nodi del grafo ordinati alfabeticamente per Name (per il menù a tendina)"""
        nodes = list(self._graph.nodes)
        nodes.sort(key=lambda x: x.Name)
        return nodes

    def getArtistaPiuInfluente(self):
        """Recupera l'artista più influente"""
        best_artist = None
        max_influenza = -float('inf') # valuto il caso in cui abbiano influenza negativa

        for nodo in self._graph.nodes:
            uscenti = self._graph.out_degree(nodo, weight='weight')
            entranti = self._graph.in_degree(nodo, weight='weight')
            influenza = uscenti - entranti

            if influenza > max_influenza:
                max_influenza = influenza
                best_artist = nodo

        return best_artist, max_influenza

    def getTop5Archi(self):
        """Restituisce i 5 archi con peso maggiore in ordine decrescente"""
        self._lista_archi.sort(key=lambda x: x.peso, reverse=True)
        return self._lista_archi[:5]
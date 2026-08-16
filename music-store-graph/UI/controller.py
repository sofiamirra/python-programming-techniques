import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceArtist = None

    def fillDDGenre(self):
        """Metodo per riempire il DropDown iniziale"""
        genres = self._model.getAllGenres()
        self._view._ddGenre.options.clear()
        genresDD = []
        for genre in genres:
            genresDD.append(ft.dropdown.Option(key=genre.GenreId, text=genre.Name))
        self._view._ddGenre.options = genresDD # assegno lista opzioni al menù a tendina
        self._view.update_page()

    def handleCreaGrafo(self, e):
        # Lettura e validazione input
        genre_id = self._view._ddGenre.value

        if genre_id is None:
            # Se l'utente non ha scelto nulla, mostro un avviso e blocco l'esecuzione
            self._view.txt_result.controls.append(ft.Text("Seleziona un genere dal menu!"))
            self._view.update_page()
            return

        # Flet restituisce i value dei dropdown come stringhe, lo converto in intero
        genre_id = int(genre_id)

        # Puliamo lo schermo dai risultati di eventuali ricerche precedenti
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Creazione del grafo in corso..."))
        self._view.update_page()

        # Creazione grafo e stampa risultati
        self._model.buildGraph(genre_id)
        n_nodi, n_archi = self._model.getGraphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato:"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {n_nodi}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {n_archi}"))

        # Recupero l'artista più influente
        best_artist, score = self._model.getArtistaPiuInfluente()
        if best_artist:
            self._view.txt_result.controls.append(
                ft.Text(f"Artista più influente: {best_artist.Name}, con influenza: {score}")
            )

        # Recupero e stampo i top 5 archi
        top_archi = self._model.getTop5Archi()
        self._view.txt_result.controls.append(ft.Text("Top 5 archi:"))
        for arco in top_archi:
            # Sfrutto il metodo __str__ della dataclass Arco per stamparlo perfettamente!
            self._view.txt_result.controls.append(ft.Text(str(arco)))

        # Popolamento DropDown Artisti
        allNodes = self._model.getAllNodes()
        self._fillDropdown(allNodes)
        self._view.update_page()

    def _fillDropdown(self, allNodes):
        """Per ciascun Artista (nodo) si crea un'opzione del menù a tendina"""
        for node in allNodes:
            # 'data' contiene l'intero oggetto, 'key' solo l'ID per il database.
            # Separiamo la logica di visualizzazione da quella di interrogazione.
            self._view._ddArtist.options.append(ft.dropdown.Option(data = node,
                                                                   text = node.Name,
                                                                   key = node.ArtistId,
                                                                   on_click=self._choiceDDArtist))

    def _choiceDDArtist(self, e):
        """Il Controller estrae l'oggetto Artist e lo salva nella variabile"""
        self._choiceArtist = e.control.data
        print(self._choiceArtist)

    def handleCammino(self,e):
        # Lettura e validazione dell'input
        artist_id = self._view._ddArtist.value

        if artist_id is None:
            self._view.txt_result.controls.append(ft.Text("Seleziona un artista dal menu!"))
            self._view.update_page()
            return

        artist_id = int(artist_id)

        # Recupero l'oggetto Artist usando la mappa che abbiamo nel Model
        artista_partenza = self._model._idMapArtists[artist_id]

        self._view.txt_result.controls.clear()
        self._view.update_page()

        # Chiamata al Model per la ricorsione
        path, score = self._model.getPath(artista_partenza)

        # Puliamo il messaggio di "ricerca in corso"
        self._view.txt_result.controls.clear()

        # Stampa dei risultati
        # Se il path ha solo 1 nodo, significa che l'algoritmo non ha trovato nessun vicino valido
        if len(path) <= 1:
            self._view.txt_result.controls.append(
                ft.Text(f"Nessun cammino valido trovato a partire da {artista_partenza.Name}.")
            )
        else:
            self._view.txt_result.controls.append(ft.Text(f"Cammino ottimo trovato!"))
            self._view.txt_result.controls.append(ft.Text(f"Numero massimo di nodi: {score}"))
            self._view.txt_result.controls.append(ft.Text("Dettaglio del percorso:"))

            # Ciclo su tutto il percorso tranne l'ultimo elemento per stampare gli archi
            for i in range(len(path) - 1):
                nodo_corrente = path[i]
                nodo_successivo = path[i + 1]

                # Vado a leggere nel grafo il peso dell'arco che unisce questi due nodi
                peso_arco = self._model._graph[nodo_corrente][nodo_successivo]['weight']
                self._view.txt_result.controls.append(
                    ft.Text(f"{nodo_corrente.Name} --> {nodo_successivo.Name} (peso: {peso_arco})")
                )

        self._view.update_page()
import flet as ft

class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDsRating(self):
        ratings = self._model.getAllRatings()
        ratingsDD = []
        for rating in ratings:
            ratingsDD.append(ft.dropdown.Option(rating))
        self._view._ddrating1.options = ratingsDD
        self._view._ddrating2.options = ratingsDD
        self._view.update_page()

    def handleCreaGrafo(self, e):
        # Lettura e validazione input
        r1 = self._view._ddrating1.value
        r2 = self._view._ddrating2.value

        if r1 is None or r2 is None:
            # Se l'utente non ha scelto nulla, mostro un avviso e blocco l'esecuzione
            self._view.txt_result.controls.append(ft.Text("Seleziona un rating dal menu!"))
            self._view.update_page()
            return

        # Flet restituisce i value dei dropdown come stringhe, lo converto in intero
        r1 = float(r1)
        r2 = float(r2)

        # Puliamo lo schermo dai risultati di eventuali ricerche precedenti
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Creazione del grafo in corso..."))
        self._view.update_page()

        # Creazione grafo e stampa risultati
        self._model.buildGraph(r1, r2)
        n_nodi, n_archi = self._model.getGraphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato:"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {n_nodi}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {n_archi}"))

        # Recupero e stampo i top 5 archi
        top_archi = self._model.getTop5Archi()
        self._view.txt_result.controls.append(ft.Text("Top 5 archi:"))
        for arco in top_archi:
            # Sfrutto il metodo __str__ della dataclass Arco per stamparlo perfettamente!
            self._view.txt_result.controls.append(ft.Text(str(arco)))

        # Stampa il numero di componenti connesse e quella maggiormente connessa
        n_comp, componente_max = self._model.getComponentiConnesseDetails()

        self._view.txt_result.controls.append(
            ft.Text(f"Il grafo ha {n_comp} componenti connesse")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"La più grande componente connessa è lunga {len(componente_max)}:")
        )

        # Itero per stampare i nomi degli attori!
        for attore in componente_max:
            self._view.txt_result.controls.append(ft.Text(f"{attore.name}"))

        self._view.update_page()

    def handleCammino(self, e):
        pass
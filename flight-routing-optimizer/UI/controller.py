import flet as ft

class Controller:
    def __init__(self, view, model):
        self._view = view # riferimento alla UI
        self._model = model # riferimento alla logica
        self._choicePartenza = None
        self._choiceArrivo = None

    def handleAnalizza(self, e):
        """Gestisce il click su Analizza Aeroporti"""
        # 1. Lettura e validazione dell'input
        cMinTxt = self._view._txtInCMin.value
        try:
            cMin = int(cMinTxt)
        except ValueError:
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(ft.Text("Inserire un valore numerico per numero minimo compagnia!"))
            self._view.update_page()
            return

        if cMin <= 0:
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(
                ft.Text("Il filtro sul numero di compagnie deve essere un intero positivo!"))
            self._view.update_page()
            return

        # Esecuzione Logica
        self._model.buildGraph(cMin)

        # Recupero Risultati e Aggiornamento UI
        nNodes, nEdges = self._model.getGraphDetails()
        self._view._txtResults.controls.clear()
        self._view._txtResults.controls.append(
            ft.Text("Grafo correttamente creato:", color="green"))
        self._view._txtResults.controls.append(
            ft.Text(f"Il grafo contiene {nNodes} nodi e {nEdges} archi."))

        # Popolamento DropDown
        allNodes = self._model.getAllNodes()
        self._fillDropdown(allNodes)
        self._view.update_page()

    def handleConnessi(self, e):
        """Gestisce il click su Aeroporti Connessi"""
        # Controllo validità input
        if self._choicePartenza is None:
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(ft.Text("Attenzione, per usare questo metodo occorre selezionare un aeroporto di partenza!", color = "red"))
            self._view.update_page()
            return

        # Chiedo al Model di restituire tutti i vicini dell'aeroporto selezionato
        viciniTupla = self._model.getViciniOrdinati(self._choicePartenza)
        self._view._txtResults.controls.clear()
        for v in viciniTupla:
            self._view._txtResults.controls.append(ft.Text(f"{v[0]} - peso {v[1]}"))
        self._view.update_page()

    def handleTestConnessione(self, e):
        """Gestisce il click su Test Connessione"""

        # Controllo validità input
        if self._choicePartenza is None:
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(
                ft.Text("Attenzione, per usare questo metodo occorre selezionare un aeroporto di partenza!", color = "red"))
            self._view.update_page()
            return

        if self._choiceArrivo is None:
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(
                ft.Text("Attenzione, per usare questo metodo occorre selezionare un aeroporto di arrivo!", color = "red"))
            self._view.update_page()
            return

        # Verifica che esista un cammino tra i due nodi (Aeroporti)
        if not self._model.hasPath(self._choicePartenza, self._choiceArrivo): # se non esiste stampa errore
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(
                ft.Text(f"Non ho trovato un cammino tra {self._choicePartenza} e {self._choiceArrivo}", color="orange"))
            self._view.update_page()
            return

        path = self._model.getPath(self._choicePartenza, self._choiceArrivo) # altrimenti cerca il cammino
        self._view._txtResults.controls.clear()
        self._view._txtResults.controls.append(
            ft.Text(f"Ho trovato un cammino tra: {self._choicePartenza} e {self._choiceArrivo}")
        )
        for p in path: # stampa i nodi che compongono il cammino
            self._view._txtResults.controls.append(ft.Text(p))
        self._view.update_page()

    def handleCerca(self, e):
        """Gestisce il click su Cerca Itinerario"""
        t = self._view._txtInNTratteMax.value # recupera il numero massimo di tratte da TextField
        try:
            tInt = int(t) # converte l'input in intero
        except ValueError:
            self._view._txtResults.controls.clear()
            self._view._txtResults.controls.append(
                ft.Text(f"Il valore di t deve essere un intero positivo", color="red")
            )
            return

        # Chiede al Model di calcolare il cammino ottimo (con score massimo)
        path, score = self._model.getCamminoOttimo(self._choicePartenza, self._choiceArrivo, tInt)
        self._view._txtResults.controls.clear()
        self._view._txtResults.controls.append(
            ft.Text(f"Cammino tra {self._choicePartenza} e {self._choiceArrivo} trovato."))
        self._view._txtResults.controls.append(
            ft.Text(f"Il cammino ha uno score complessivo pari a {score} e contiene i seguenti nodi:"))
        for p in path:
            self._view._txtResults.controls.append(ft.Text(p))
        self._view.update_page()

    def _fillDropdown(self, allNodes):
        """Per ciascun Aeroporto (nodo) si crea un'opzione del menù a tendina"""
        for node in allNodes:
            self._view._ddAeroportoP.options.append(ft.dropdown.Option(data=node,
                                                                       key= node.IATA_CODE,
                                                                       on_click=self._choiceDdPartenza))

            self._view._ddAeroportoA.options.append(ft.dropdown.Option(data=node,
                                                                       key=node.IATA_CODE,
                                                                       on_click=self._choiceDdArrivo))

    def _choiceDdPartenza(self, e):
        """Il Controller estrae l'oggetto Airport e lo salva nella variabile"""
        self._choicePartenza = e.control.data

    def _choiceDdArrivo(self, e):
        self._choiceArrivo = e.control.data
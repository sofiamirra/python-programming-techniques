import flet as ft

class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def _fillDDYears(self):
        """Riempie i menu a tendina della vista con gli anni recuperati dal modello e aggiorna l'interfaccia grafica"""
        years = self._model.getAllYears() # chiamata al modello per ottenere la lista di anni dal database
        yearsDD = []
        for year in years: # ciclo per trasformare ogni anno in un elemento grafico selezionabile
            yearsDD.append(ft.dropdown.Option(year))
        # assegnazione della lista di opzioni ai menu a tendina
        self._view._ddAnno1.options = yearsDD
        self._view._ddAnno2.options = yearsDD
        self._view.update_page()

    def handleCreaGrafo(self,e):
        """"Legge i parametri scelti e crea la struttura"""
        # lettura dei valori dai menu a tendina della vista
        year1 = self._view._ddAnno1.value
        year2 = self._view._ddAnno2.value
        self._model.buildGraph(year1, year2)
        self._view.txt_result.controls.clear() # pulisco prima di stampare qualsiasi cosa
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato", color="red"))

        nNodes, nEdges = self._model.getGraphDetails()
        self._view.txt_result.controls.append(ft.Text(f"Numero nodi: {nNodes}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero archi: {nEdges}"))
        self._view.update_page() # rendering dei cambiamenti

    def handleDettagli(self, e):
        self._view.txt_result.controls.clear() # pulisco prima di stampare qualsiasi cosa
        self._view.txt_result.controls.append(ft.Text("Archi di peso maggiore: ", color="red"))
        top_archi = self._model.getTop3Archi()
        for arco in top_archi:
            # Metodo di stampa definito in __str__ di arco
            self._view.txt_result.controls.append(ft.Text(str(arco)))

        nComp,  bComp, nodes = self._model.getComponentiConnesseDetails()
        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {nComp} componenti connesse", color="red"))
        self._view.txt_result.controls.append(ft.Text(f"Componente più grande ({len(nodes)} nodi): ", color="red"))
        for node in nodes:
            self._view.txt_result.controls.append(ft.Text(f"{node.driverRef} ({node.driverId}) -- DoB: {node.dob}"))

        self._view.txt_result.controls.append(ft.Text(f"Componente connessa in ordine decrescente: ", color="red"))
        for node in nodes:
            grado = self._model._graph.degree(node)
            self._view.txt_result.controls.append(ft.Text(f"{node.driverRef} ({node.driverId}) -- DoB: {node.dob} (grado={grado})"))
        self._view.update_page()

    def handleCerca(self, e):
        self._view.txt_result.controls.clear()
        k = self._view._txtInK.value # prendo il valore dal campo di testo

        # Validazione con return
        if k is None or k == "":
            self._view.txt_result.controls.append(ft.Text("Attenzione! Inserire un valore intero!", color="red"))
            self._view.update_page()
            return

        try:
            kInt = int(k)
        except ValueError:
            self._view.txt_result.controls.append(ft.Text("Attenzione! Inserire un valore intero!", color="red"))
            self._view.update_page()
            return

        listaPilotiOttima, minDistEta = self._model.getListaPilotiOttima(kInt)

        if listaPilotiOttima is None:
            self._view.txt_result.controls.append(ft.Text(
                f"Non ci sono abbastanza componenti connesse per trovare {kInt} piloti "
                f"che NON siano stati compagni di squadra nel range selezionato", color="red"))
            self._view.update_page()
            return

            # 5. Stampa in caso di successo
        self._view.txt_result.controls.append(
            ft.Text("Lista di piloti con scarto di età minimo (mai stati compagni di squadra):", color="green"))

        # Ciclo pulito senza return interno
        for p in listaPilotiOttima:
            self._view.txt_result.controls.append(ft.Text(str(p)))

        # Trovo min e max (usando la funzione lambda sulla data di nascita)
        youngest = min(listaPilotiOttima, key=lambda x: x.dob)
        oldest = max(listaPilotiOttima, key=lambda x: x.dob)
        self._view.txt_result.controls.append(
            ft.Text(f"Differenza di età tra pilota più giovane e pilota più anziano: {minDistEta}"))
        self._view.txt_result.controls.append(ft.Text(f"Pilota più giovane: {youngest}"))
        self._view.txt_result.controls.append(ft.Text(f"Pilota più anziano: {oldest}"))
        self._view.update_page()




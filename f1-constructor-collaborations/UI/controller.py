import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def _fillDDYears(self):
        years = self._model.getYears()
        yearsDD = []
        for year in years:
            yearsDD.append(ft.dropdown.Option(year))
        self._view._ddAnno1.options = yearsDD
        self._view._ddAnno2.options = yearsDD
        self._view.update_page()

    def handleCreaGrafo(self,e):
        year1 = self._view._ddAnno1.value
        year2 = self._view._ddAnno2.value
        self._model.buildGraph(year1, year2)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato!", color="red"))

        nNodes, nEdges = self._model.getGraphDetails()
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {nNodes}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {nEdges}"))
        self._view.update_page()

    def handleDettagli(self, e):
        self._view.txt_result.controls.clear()  # pulisco prima di stampare qualsiasi cosa
        self._view.txt_result.controls.append(ft.Text("Archi di peso maggiore: ", color="red"))
        top_archi = self._model.getTop3Archi()
        for arco in top_archi:
            # Metodo di stampa definito in __str__ di arco
            self._view.txt_result.controls.append(ft.Text(str(arco)))

        nComp,  bComp, nodes = self._model.getComponentiConnesseDetails()
        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {nComp} componenti connesse", color="red"))
        self._view.txt_result.controls.append(ft.Text(f"Componente più grande ({len(nodes)} nodi): ", color="red"))
        for node in nodes:
            self._view.txt_result.controls.append(ft.Text(f"{node.constructorRef} ({node.name})"))
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

        listaSquadreOttima, minDistEta = self._model.getListaSquadreOttima(kInt)

        if listaSquadreOttima is None or len(listaSquadreOttima) == 0:
            self._view.txt_result.controls.append(ft.Text(
                f"Attenzione: Non ci sono abbastanza piloti con date valide per formare {kInt} squadre "
                f"che NON siano state compagne di squadra nel range selezionato.", color="red"))
            self._view.update_page()
            return

        # Stampa in caso di successo
        self._view.txt_result.controls.append(ft.Text("Lista dei K costruttori selezionati:", color="green"))

        # Ciclo pulito senza return interno
        for s in listaSquadreOttima:
            self._view.txt_result.controls.append(ft.Text(str(s)))

        # Trovo min e max (usando la funzione lambda sulla data di nascita)
        youngest = max(listaSquadreOttima, key=lambda x: x.oldest_driver_dob)
        oldest = min(listaSquadreOttima, key=lambda x: x.oldest_driver_dob)
        self._view.txt_result.controls.append(
            ft.Text(f"Differenza di età tra i piloti: {minDistEta}"))
        self._view.txt_result.controls.append(ft.Text(f"Squadra con il pilota più giovane: {youngest}"))
        self._view.txt_result.controls.append(ft.Text(f"Squadra con il pilota più anziano: {oldest}"))
        self._view.update_page()



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
        self._view._ddYear1.options = yearsDD
        self._view._ddYear2.options = yearsDD
        self._view.update_page()

    def handleBuildGraph(self, e):
        year1 = self._view._ddYear1.value
        year2 = self._view._ddYear2.value
        if year1 is None or year2 is None:
            self._view.create_alert("Seleziona entrambi gli anni!")
            return

        try:
            year1 = int(year1)
            year2 = int(year2)
        except ValueError:
            self._view.create_alert("Seleziona entrambi gli anni!")

        self._model.buildGraph(year1, year2)
        self._view._txtGraphDetails.controls.clear()
        self._view._txtGraphDetails.controls.append(ft.Text("Grafo correttamente creato."))

        nNodes, nEdges = self._model.getGraphDetails()
        self._view._txtGraphDetails.controls.append(ft.Text(f"Il grafo contiene {nNodes} nodi e {nEdges} archi"))
        self._view.update_page()

    def handlePrintDetails(self, e):
        self._view._txtGraphDetails.controls.clear()
        bComp, nodes, min_weights = self._model.getComponentiConnesseDetails()
        self._view._txtGraphDetails.controls.append(ft.Text(f"Stampa dettagli: "))
        for node in nodes:
            peso_min = min_weights.get(node, 0)
            self._view._txtGraphDetails.controls.append(ft.Text(f"{node.name} -- ({peso_min})"))
        self._view.update_page()

    def handleCercaDreamChampionship(self, e):
        pass


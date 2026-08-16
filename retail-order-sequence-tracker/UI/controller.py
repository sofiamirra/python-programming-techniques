import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def _fillDDStores(self):
        stores = self._model.getStore()
        storesDDOptions = list(
            map(lambda x: ft.dropdown.Option(data=x, key=x.store_id, text=x.store_name, on_click=self._choiceStore), stores))
        self._view._ddStore.options = storesDDOptions
        self._view.update_page()

    def _choiceStore(self, e):
        self._storeValue = e.control.data

    def handleCreaGrafo(self, e):
        storeId = self._view._ddStore.value
        k_str = self._view._txtIntK.value

        # Controllo Dropdown
        if storeId is None:
            self._view.create_alert("Seleziona uno Store dal menù!")
            return

        # Controllo intero (con Try-Except)
        try:
            k = int(k_str)
        except ValueError:
            self._view.create_alert("Il valore di K deve essere un numero intero!")
            return

        self._model.buildGraph(storeId, k)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato: "))

        nNodes, nEdges = self._model.getGraphDetails()
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {nNodes}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {nEdges}"))
        self._view.update_page()
        self._view.txt_result.controls.append(ft.Text("5 achi di peso maggiore: "))
        top_archi = self._model.getTop5Archi()
        for arco in top_archi:
            self._view.txt_result.controls.append(ft.Text(f"Arco: {str(arco)}"))
        self._view.update_page()
        self._fillDDNodes(storeId)

    def _fillDDNodes(self, storeId):
        nodes = self._model.getAllNodes(storeId)
        nodesDDOptions = list(
            map(lambda x: ft.dropdown.Option(data=x, key=x.order_id, on_click=self._choiceNode), nodes))
        self._view._ddNode.options = nodesDDOptions
        self._view._ddNode.disabled = False
        self._view._btnCerca.disabled = False
        self._view._btnRicorsione.disabled = False
        self._view.update_page()

    def _choiceNode(self, e):
        self._nodeValue = e.control.data

    def handleCerca(self, e):
        sourceStr = self._view._ddNode.value

        if sourceStr is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Errore: selezionare un nodo di partenza", color="red")
            )
            self._view.update_page()
            return

        cammino = self._model.getCammino(sourceStr)

        self._view.txt_result.controls.clear()
        if not cammino:  # Se la lista è vuota
            self._view.txt_result.controls.append(ft.Text("Nessun percorso trovato per questo nodo!", color="orange"))
        else:
            self._view.txt_result.controls.append(ft.Text(f"Nodo di partenza: {sourceStr}", color="red"))
            for nodo in cammino:
                self._view.txt_result.controls.append(ft.Text(str(nodo)))

    def handleRicorsione(self, e):
        source = self._nodeValue

        if source is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Errore: selezionare un nodo di partenza", color="red"))
            self._view.update_page()
            return

        path, score = self._model.getPercorsoDecrescentePesoMassimo(source)

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Percorso migliore trovato: score = {score}", color="red"))

        for nodo in path:
            self._view.txt_result.controls.append(ft.Text(str(nodo)))

        self._view.update_page()

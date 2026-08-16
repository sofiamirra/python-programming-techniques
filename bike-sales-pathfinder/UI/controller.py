import datetime

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def _fillDDCategories(self):
        categories = self._model.getCategories()
        categoriesDDOptions = list(
            map(lambda x: ft.dropdown.Option(data=x, key=x.category_id, text=x.category_name, on_click=self._choiceCategory), categories))
        self._view._ddcategory.options = categoriesDDOptions
        self._view.update_page()

    def _choiceCategory(self, e):
        self._categoryValue = e.control.data

    def handleCreaGrafo(self, e):
        date1 = self._view._dp1.value
        date2 = self._view._dp2.value
        category = self._view._ddcategory.value

        if category is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Errore: selezionare la categoria", color="red")
            )
            self._view.update_page()
            return


        if date1 is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Errore: selezionare la prima data", color="red")
            )
            self._view.update_page()
            return

        if date2 is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Errore: selezionare la seconda data", color="red")
            )
            self._view.update_page()
            return

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Date selezionate: "))
        self._view.txt_result.controls.append(ft.Text(date1.date()))
        self._view.txt_result.controls.append(ft.Text(date2.date()))

        self._model.buildGraph(category, date1, date2)

        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato: "))

        nNodes, nEdges = self._model.getGraphDetails()
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {nNodes}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {nEdges}"))
        self._fillDDProducts(category)
        self._view.update_page()

    def handleBestProdotti(self, e):
        bestProdotti = self._model.getBestSellers()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("I cinque prodotti più venduti sono: "))
        for p in bestProdotti:
            self._view.txt_result.controls.append(ft.Text(f"{p[0]} with score {p[1]}"))
        self._view.update_page()

    def handleCercaCammino(self, e):
        source = self._view._ddProdStart.value
        target = self._view._ddProdEnd.value
        k = self._view._txtInLun.value

        if source is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Errore: selezionare un prodotto di partenza", color="red")
            )
            self._view.update_page()
            return

        if target is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Errore: selezionare un prodotto di destinazione", color="red")
            )
            self._view.update_page()
            return

        if k is None or k == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Errore: inserire la lunghezza del cammino", color="red")
            )
            self._view.update_page()
            return

        try:
            k = int(k)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Errore: la lunghezza deve essere un numero intero", color="red")
            )
            self._view.update_page()
            return

        if k <= 0:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Errore: la lunghezza deve essere maggiore di zero", color="red")
            )
            self._view.update_page()
            return

        path, score = self._model.getPercorso(source, target, k)

        if path is None or len(path) == 0:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Nessun cammino trovato tra i due prodotti con la lunghezza richiesta", color="red")
            )
            self._view.update_page()
            return

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Percorso migliore trovato con score = {score} e lunghezza = {k}", color="red")
        )

        for nodo in path:
            self._view.txt_result.controls.append(ft.Text(str(nodo)))

        self._view.update_page()

    def _fillDDProducts(self, idCategory):
        products = self._model.getNodes(idCategory)
        productsDDOptions = list(
            map(lambda x: ft.dropdown.Option(data=x, key=x.product_id, text=x.product_name, on_click=self._choiceProduct), products))
        self._view._ddProdStart.options = productsDDOptions
        self._view._ddProdEnd.options = productsDDOptions
        self._view.update_page()

    def _choiceProduct(self, e):
        self._productValue = e.control.data

    def setDates(self):
        first, last = self._model.getDateRange()

        self._view._dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view._dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp2.current_date = datetime.date(last.year, last.month, last.day)

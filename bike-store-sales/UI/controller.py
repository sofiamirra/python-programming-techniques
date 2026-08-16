import datetime

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCreaGrafo(self, e):
        category = self._categoryValue
        date1 = self._view._dp1.value
        date2 = self._view._dp2.value
        self._model.buildGraph(category, date1, date2)
        nNodi, nArchi = self._model.getGraphDetails()

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Date Selezionate: "))
        self._view.txt_result.controls.append(ft.Text(f"Start Date: {self._view._dp1.value.date()}"))
        self._view.txt_result.controls.append(ft.Text(f"End Date: {self._view._dp2.value.date()}"))
        self._view.txt_result.controls.append(ft.Text("Grafo Creato"))
        self._view.txt_result.controls.append(ft.Text(f"Numero nodi: {nNodi}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero archi: {nArchi}"))
        self._view.update_page()
        self._fillDDProdotti()

    def handleBestProdotti(self, e):
        bestProdotti = self._model.getBestSellers()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Prodotti maggiormente profittevoli: "))
        for p in bestProdotti:
            self._view.txt_result.controls.append(ft.Text(f"{p[0]} - score = {p[1]}"))
        self._view.update_page()

    def handleCercaCammino(self, e):
        # Controllo sull'input utente (lunghezza fissa)
        if self._view._txtInLun.value == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione, inserire un valore numerico!"))
            self._view.update_page()
            return

        # Controllo sul tipo di dato
        try:
            lun = int(self._view._txtInLun.value)
        except ValueError:
            # Se l'utente ha scritto "ciao" o "5.5", Python lancia un ValueError
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Attenzione, inserire un valore numerico!"))
            self._view.update_page()
            return

        # chiamata al Model
        path, score = self._model.getBestPath(lun, self._prodStartValue, self._prodEndValue)

        if len(path) == 0: # gestione risultato vuoto
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Non ho trovato un cammino tra {self._prodStartValue} e {self._prodEndValue}"))
            self._view.update_page()
            return

        # stampa del successo
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Cammino migliore tra {self._prodStartValue} e {self._prodEndValue}"))
        for p in path:
            self._view.txt_result.controls.append(ft.Text(p))
        self._view.txt_result.controls.append(ft.Text(f"Score: {score}"))
        self._view.update_page()

    def _fillDDCategories(self):
        categories = self._model.getCategories() # Recupero la lista di oggetti dal Model
        # Trasformo ogni oggetto 'x' in una Option di Flet
        categoriesDDOptions = list(map(lambda x:ft.dropdown.Option(data=x, key=x.category_name, on_click=self._choiceCategory), categories))
        self._view._ddcategory.options = categoriesDDOptions # Assegno la lista al Dropdown nella View
        self._view.update_page()

    def _choiceCategory(self, e):
        # Metodo che gestisce il click dell'utente
        self._categoryValue = e.control.data

    def _fillDDProdotti(self):
        prodotti = self._model.getAllNodes()
        nodesDDOptionStart = list(map(lambda x:ft.dropdown.Option(data=x, key=x.product_name, on_click=self._choiceProdStart), prodotti))
        nodesDDOptionEnd = list(map(lambda x: ft.dropdown.Option(data=x, key=x.product_name, on_click=self._choiceProdEnd), prodotti))
        self._view._ddProdStart.options = nodesDDOptionStart
        self._view._ddProdEnd.options = nodesDDOptionEnd
        self._view.update_page()

    def _choiceProdStart(self, e):
        self._prodStartValue = e.control.data

    def _choiceProdEnd(self, e):
        self._prodEndValue = e.control.data

    def setDates(self):
        first, last = self._model.getDateRange()

        self._view._dp1.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp1.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp1.current_date = datetime.date(first.year, first.month, first.day)

        self._view._dp2.first_date = datetime.date(first.year, first.month, first.day)
        self._view._dp2.last_date = datetime.date(last.year, last.month, last.day)
        self._view._dp2.current_date = datetime.date(last.year, last.month, last.day)

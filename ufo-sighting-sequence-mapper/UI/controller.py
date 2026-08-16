import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def _fillDDYears(self):
        years = self._model.getAllYears()
        yearsDD = []
        for year in years:
            yearsDD.append(ft.dropdown.Option(year))
        self._view.ddyear.options = yearsDD
        self._view.update_page()

    def _fillDDStates(self, year):
        states = self._model.getAllStates(year)
        statesDDOptions = list(map(lambda x: ft.dropdown.Option(data=x, key=x._Name, on_click=self._choiceState), states))
        self._view.ddstate.options = statesDDOptions
        self._view.update_page()

    def handle_year_selection(self, e):
        """Metodo collegato a on_change della View"""
        year = self._view.ddyear.value
        if year is None:
            return
        self._fillDDStates(year)

    def _choiceState(self, e):
        self._stateValue = e.control.data

    def handle_graph(self, e):
        year = self._view.ddyear.value
        state = self._view.ddstate.value
        self._model.buildGraph(year, state)
        self._view.txt_result1.controls.clear()
        self._view.txt_result1.controls.append(ft.Text("Grafo correttamente creato!"))

        nNodes, nEdges = self._model.getGraphDetails()
        self._view.txt_result1.controls.append(ft.Text(f"Numero di vertici: {nNodes}"))
        self._view.txt_result1.controls.append(ft.Text(f"Numero di archi: {nEdges}"))
        self._view.update_page()

    def handle_path(self, e):
        self._view.txt_result1.controls.clear()  # pulisco prima di stampare qualsiasi cosa
        nComp, bComp, nodes = self._model.getComponentiConnesse()
        self._view.txt_result1.controls.append(ft.Text(f"Il grafo ha {nComp} componenti connesse"))
        self._view.txt_result1.controls.append(ft.Text(f"La componente connessa più grande è costituita da ({len(nodes)} nodi): "))
        for node in nodes:
            self._view.txt_result1.controls.append(ft.Text(str(node)))
        self._view.update_page()



import flet as ft
from UI.view import View
from model.modello import Model

class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view: View = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def _fillDDShape(self):
        shapes = self._model.getShapes()
        shapeDD = []
        for shape in shapes:
            shapeDD.append(ft.dropdown.Option(shape))
        self._view.ddshape.options = shapeDD
        self._view.update_page()

    def handle_graph(self, e):
        lat = self._view.txt_latitude.value
        lng = self._view.txt_longitude.value
        shape =  self._view.ddshape.value

        if shape is None:
            self._view.txt_result1.controls.clear()
            self._view.txt_result1.controls.append(
                ft.Text("Errore: selezionare una forma dal menù", color="red")
            )
            self._view.update_page()
            return

        if lat is None or lat == "":
            self._view.txt_result1.controls.clear()
            self._view.txt_result1.controls.append(
                ft.Text("Errore: inserire un valore per la latitudine", color="red")
            )
            self._view.update_page()
            return

        if lng is None or lng == "":
            self._view.txt_result1.controls.clear()
            self._view.txt_result1.controls.append(
                ft.Text("Errore: inserire un valore per la longitudine", color="red")
            )
            self._view.update_page()
            return

        try:
            lat = float(lat)
        except ValueError:
            self._view.txt_result1.controls.clear()
            self._view.txt_result1.controls.append(
                ft.Text("Errore: Latitdine deve essere un numero", color="red")
            )
            self._view.update_page()
            return

        try:
            lng = float(lng)
        except ValueError:
            self._view.txt_result1.controls.clear()
            self._view.txt_result1.controls.append(
                ft.Text("Errore: Longitudine deve essere un numero", color="red")
            )
            self._view.update_page()
            return

        dictValues = self._model.getValues()
        if lat > dictValues["max_latitude"] or lat < dictValues["min_latitude"]:
            self._view.txt_result1.controls.clear()
            self._view.txt_result1.controls.append(
                ft.Text(f"La latitudine deve essere un valore compreso tra {dictValues["min_latitude"]} e {dictValues["max_latitude"]}", color="red")
            )
            self._view.update_page()
            return

        if lng > dictValues["max_longitude"] or lng < dictValues["min_longitude"]:
            self._view.txt_result1.controls.clear()
            self._view.txt_result1.controls.append(
                ft.Text(f"La longitudine deve essere un valore compreso tra {dictValues["min_longitude"]} e {dictValues["max_longitude"]}", color="red")
            )
            self._view.update_page()
            return

        self._model.buildGraph(shape, lat, lng)
        self._view.txt_result1.controls.clear()
        self._view.txt_result1.controls.append(ft.Text("Grafo correttamente creato!"))

        nNodes, nEdges = self._model.getGraphDetails()
        self._view.txt_result1.controls.append(ft.Text(f"Numero di nodi: {nNodes}"))
        self._view.txt_result1.controls.append(ft.Text(f"Numero di archi: {nEdges}"))
        self._view.update_page()

        self._view.txt_result1.controls.append(ft.Text("I 5 nodi di grado maggiore sono: "))
        top_nodi = self._model.getTop5Nodi()
        for nodo in top_nodi:
            grado = self._model._graph.degree(nodo)
            self._view.txt_result1.controls.append(ft.Text(f"{nodo.Name} --> degree: {grado}"))
        self._view.update_page()

        self._view.txt_result1.controls.append(ft.Text("I 5 archi di peso maggiore sono: "))
        top_archi = self._model.getTop5Archi()
        for arco in top_archi:
            self._view.txt_result1.controls.append(ft.Text(str(arco)))
        self._view.btn_path.disabled = False
        self._view.update_page()


    def handle_path(self, e):
        path, score = self._model.getPercorso()

        self._view.txt_result2.controls.clear()

        if path is None or len(path) == 0:
            self._view.txt_result2.controls.append(
                ft.Text("Nessun percorso trovato", color="red")
            )
            self._view.update_page()
            return

        self._view.txt_result2.controls.append(
            ft.Text(f"Punteggio totale del percorso: {score}", color="red")
        )

        self._view.txt_result2.controls.append(
            ft.Text("Stati attraversati:")
        )

        for stato in path:
            densita = self._model.getDensita(stato)
            self._view.txt_result2.controls.append(
                ft.Text(f"{stato} - densità: {densita:.4f}")
            )

        dettagli = self._model.getPathDetails(path)

        self._view.txt_result2.controls.append(
            ft.Text("Archi attraversati:")
        )

        for n1, n2, peso, distanza in dettagli:
            self._view.txt_result2.controls.append(
                ft.Text(f"{n1} --> {n2} | peso: {peso:.2f} | distanza: {distanza}")
            )

        self._view.update_page()

    def fill_ddshape(self):
        pass

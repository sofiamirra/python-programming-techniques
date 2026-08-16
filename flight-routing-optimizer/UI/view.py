import flet as ft

class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # Inizializzare impostazioni di pagina
        self._page = page
        self._page.title = "TdP Flights Manager 2026"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        self._page.window_width = 1000
        # Controller non si inzializza: resta None
        self._controller = None
        # Elementi grafici (opzionali)
        self._title = None

    def load_interface(self):
        """Si costruisce l'interfaccia grafica con i suoi elementi"""
        self._title = ft.Text("TdP Flights Manager 2026", color="blue", size=24)
        self._page.controls.append(self._title)

        # Inizializzazione Elementi - ROW 1
        self._txtInCMin = ft.TextField(label ="N min compagnie")
        self._btnAnalizzaAeroporti = ft.ElevatedButton(text="Analizza",
                                                       on_click=self._controller.handleAnalizza) # collegamento Controller
        row1 = ft.Row([ # inseriamo gli elementi nella riga
            ft.Container(content= None, width=250), # primo container vuoto per lasciare spazio
            ft.Container(self._txtInCMin, width=250),
            ft.Container(self._btnAnalizzaAeroporti, width=250) ],
            alignment=ft.MainAxisAlignment.CENTER)

        # Inizializzazione Elementi - ROW 2
        self._ddAeroportoP = ft.Dropdown(label="Aeroporto di Partenza")
        self._btnAeroportiConnessi = ft.ElevatedButton(text="Aeroporti Connessi",
                                                       on_click=self._controller.handleConnessi) # collegamento Controller
        self._ddAeroportoA = ft.Dropdown(label="Aeroporto di Destinazione")
        self._btnTestConnessione = ft.ElevatedButton(text="Test Connessione",
                                                     on_click=self._controller.handleTestConnessione)

        row2 = ft.Row([ # inseriamo gli elementi nella riga
            ft.Container(content=None, width=250), # primo container vuoto per lasciare spazio
            ft.Container(self._ddAeroportoP, width=150),
            ft.Container(self._btnAeroportiConnessi, width=150),
            ft.Container(self._ddAeroportoA, width=150),
            ft.Container(self._btnTestConnessione, width=150)],
            alignment=ft.MainAxisAlignment.CENTER)

        # Inizializzazione Elementi - ROW 3
        self._txtInNTratteMax = ft.TextField(label="Num Tratte Max")
        self._btnCercaItinerario = ft.ElevatedButton(text="Cerca Itinerario",
                                                       on_click=self._controller.handleCerca)

        row3 = ft.Row([
            ft.Container(content=None),
            ft.Container(self._txtInNTratteMax, width=250),
            ft.Container(self._btnCercaItinerario, width=250),],
            alignment=ft.MainAxisAlignment.CENTER)

        # List View
        self._txtResults = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.add(row1, row2, row3, self._txtResults)
        self._page.update()

    """Metodi di supporto al codice (getter/setter/alert)"""
    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()

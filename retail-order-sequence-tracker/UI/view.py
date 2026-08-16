import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "TdP -- Appello straordinario del 10/11/2025"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        self._page.bgcolor = "#ebf4f4"
        self._page.window_height = 800
        page.window_center()
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None
        self._txt_name = None
        self._txt_result = None

    def load_interface(self):
        # title
        self._title = ft.Text("Appello straordinario del 10/11/2025", color="blue", size=24)
        self._page.controls.append(self._title)

        self._ddStore = ft.Dropdown(label="Store", width=250)
        self._controller._fillDDStores()
        self._txtIntK = ft.TextField(label="K", width=100)
        self._ddNode = ft.Dropdown(label="Node", width=150, disabled=True)

        row1 = ft.Row([self._ddStore, self._txtIntK, self._ddNode], alignment=ft.MainAxisAlignment.CENTER,
                      vertical_alignment=ft.CrossAxisAlignment.END)

        self._btnCreaGrafo = ft.ElevatedButton(text="Crea Grafo", on_click=self._controller.handleCreaGrafo)
        self._btnCerca = ft.ElevatedButton(text="Cerca Percorso Massimo",
                                           on_click=self._controller.handleCerca, disabled=True)
        self._btnRicorsione = ft.ElevatedButton(text="Ricorsione",
                                           on_click=self._controller.handleRicorsione, disabled=True)

        row2 = ft.Row([self._btnCreaGrafo, self._btnCerca, self._btnRicorsione], alignment=ft.MainAxisAlignment.CENTER)

        self._page.controls.append(row1)
        self._page.controls.append(row2)
        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self.txt_result)
        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def update_page(self):
        self._page.update()
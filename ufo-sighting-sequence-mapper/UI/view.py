import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "TdP 2024 - Esame del 04/07/2024 - B"
        self._page.horizontal_alignment = 'CENTER'
        self._page.window_width = 950
        self._page.theme_mode = ft.ThemeMode.LIGHT
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # title
        self._title = None
        # first row
        self.ddyear = None
        self.ddstate = None
        self.btn_graph = None
        self.btn_path = None
        # second row
        self.txt_result1 = None  # Qui scrivere gli outputs del punto 1
        self.txt_result2 = None  # Qui scrivere gli outputs del punto 2

    def load_interface(self):
        # title
        self._title = ft.Text("TdP 2024 - Esame del 04-07-2024 - B", color="blue", size=24)
        self._page.controls.append(self._title)

        # First row with some controls
        self.ddyear = ft.Dropdown(label="Anno",
                                  hint_text="Anno da analizzare per gli avvistamenti.",
                                  on_change = self._controller.handle_year_selection)
        self._controller._fillDDYears()
        self.ddstate = ft.Dropdown(label="Stato",
                                   hint_text="Stato da analizzare per gli avvistamenti.")
        self.btn_graph = ft.ElevatedButton(text="Crea Grafo",
                                           tooltip="Crea il grafo del punto 1",
                                           on_click=self._controller.handle_graph)
        self.btn_path = ft.ElevatedButton(text="Calcola percorso",
                                          tooltip="Risolvi il punto 2",
                                          on_click=self._controller.handle_path)

        row1 = ft.Row([self.ddyear, self.ddstate, self.btn_graph, self.btn_path],
                      alignment=ft.MainAxisAlignment.SPACE_EVENLY)
        self._page.controls.append(row1)

        # List View where the reply is printed
        self.txt_result1 = ft.ListView(width=400, expand=1, spacing=10, padding=20, auto_scroll=False)
        self.txt_result2 = ft.ListView(width=400, expand=1, spacing=10, padding=20, auto_scroll=False)
        self.txt_result1.controls.append(ft.Text("Risultati punto1"))
        self.txt_result2.controls.append(ft.Text("Risultati punto2"))

        container1 = ft.Container(
            content=self.txt_result1,
            margin=10,
            padding=10,
            alignment=ft.alignment.center,
            bgcolor=ft.colors.GREY_200,
            width=450,
            height=450,
            border_radius=10,
        )
        container2 = ft.Container(
            content=self.txt_result2,
            margin=10,
            padding=10,
            alignment=ft.alignment.center,
            bgcolor=ft.colors.GREY_200,
            width=450,
            height=450,
            border_radius=10,
        )

        row2 = ft.Row([container1, container2],
                      alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                      spacing=50)
        self._page.controls.append(row2)
        self._page.update()

        self._page.update()

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

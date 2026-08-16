import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "Esame del 15/09/2025"
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
        self.txt_result = None

    def load_interface(self):
        # title
        self._title = ft.Text("Esame del 15/09/2025", color="blue", size=24)
        self._page.controls.append(self._title)

        self._ddAnno1 = ft.Dropdown(label="Da", hint_text="Anno")
        self._ddAnno2 = ft.Dropdown(label="A", hint_text="Anno")
        self._controller._fillDDYears()
        self._btnCreaGrafo = ft.ElevatedButton(text="Crea Grafo", on_click=self._controller.handleCreaGrafo)


        cont1 = ft.Container(self._ddAnno1, width=250)
        cont2 = ft.Container(self._ddAnno2, width=250)
        row1 = ft.Row([cont1,cont2, self._btnCreaGrafo], alignment=ft.MainAxisAlignment.CENTER,
                      vertical_alignment=ft.CrossAxisAlignment.END)

        self._btnstampa = ft.ElevatedButton(text="Stampa Dettagli",
                                           on_click=self._controller.handleDettagli)
        row2 = ft.Row([ft.Container(self._btnstampa, width=250)
                       ], alignment=ft.MainAxisAlignment.CENTER)


        self._txtInK = ft.TextField(label="Num di piloti")
        self._btnCerca = ft.ElevatedButton(text="Cerca lista piloti",
                                           on_click=self._controller.handleCerca)
        row3 = ft.Row([ft.Container(self._txtInK, width=250), ft.Container(self._btnCerca, width=250)], alignment=ft.MainAxisAlignment.CENTER)

        self._page.controls.append(row1)
        self._page.controls.append(row2)
        self._page.controls.append(row3)
        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self.txt_result)
        self._page.update()

    def set_controller(self, controller):
        self._controller = controller

    def update_page(self):
        self._page.update()
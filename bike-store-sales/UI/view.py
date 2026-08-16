from datetime import datetime

import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "Esame del 10/07/2025 - Turno A"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        self._page.bgcolor = "#ebf4f4"
        self._page.window_height = 600
        self._page.window_width = 1000
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None
        self.txt_name = None
        self.btn_hello = None
        self.txt_result = None
        self.txt_container = None

    def load_interface(self):
        # title
        self._title = ft.Text("Esame del 10/07/2025 - Turno A", color="green", size=24)
        self._page.controls.append(self._title)

        self._ddcategory = ft.Dropdown(label="Category", width=200)
        self._controller._fillDDCategories()

        self._dp1 = ft.DatePicker(
            on_change=lambda e: print(f"Giorno selezionato: {self._dp1.value}"),
            on_dismiss=lambda e: print("Data non selezionata")
        )

        self._page.overlay.append(self._dp1)
        self._btnCal1 = ft.ElevatedButton("Start date",
                                              icon=ft.icons.CALENDAR_MONTH,
                                              on_click=lambda _: self._dp1.pick_date())

        self._dp2 = ft.DatePicker(
            on_change=lambda e: print(f"Giorno selezionato: {self._dp2.value}"),
            on_dismiss=lambda e: print("Data non selezionata")
        )
        self._page.overlay.append(self._dp2)
        self._btnCal2 = ft.ElevatedButton("End date",
                                              icon=ft.icons.CALENDAR_MONTH,
                                              on_click=lambda _: self._dp2.pick_date())

        self._controller.setDates()

        self._btnCreaGrafo = ft.ElevatedButton(text="Crea Grafo", on_click=self._controller.handleCreaGrafo)

        self._btnBestProdotti = ft.ElevatedButton(text="Prodotti più venduti",
                                           on_click=self._controller.handleBestProdotti)

        row1 = ft.Row([self._ddcategory, self._btnCal1, self._btnCal2, self._btnCreaGrafo, self._btnBestProdotti],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row1)

        self._txtInLun = ft.TextField(label="Lunghezza cammino", width=120)
        self._ddProdStart = ft.Dropdown(label="Start product", width=350)
        self._ddProdEnd = ft.Dropdown(label="End product", width=350)

        self._btnCercaCammino = ft.ElevatedButton(text="Cerca ",
                                                  on_click=self._controller.handleCercaCammino, width=120)

        row2 = ft.Row([self._txtInLun, self._ddProdStart, self._ddProdEnd, self._btnCercaCammino],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row2)

        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=False)
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

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()

import os
from tkinter import ttk

from utils.buildResolve import resolve_route


class Resources:
    def __init__(self, root):
        self.root = root
        print("hola")
        self.resources_frame = ttk.Frame(self.root)
        self.resources_frame.pack(pady=10)
        self.pdf_button = self.create_pdf_button()
        self.excel_button = self.create_excel_button()
        self.creditos = ttk.Label(
            self.resources_frame,
            text="Desarrollado por: Álvaro Huertas Díaz"
        )
        self.creditos.pack(pady=15)


    def create_pdf_button(self):
        pdf_button = ttk.Button(
            self.resources_frame,
            text="Diseño de registro model 182.pdf",
            command=lambda: os.startfile(
                filepath=resolve_route('assets/disegno_de_registro_182.pdf')
            )
        )
        pdf_button.pack(padx=5, pady=5)

        return pdf_button

    def create_excel_button(self):
        excel_button = ttk.Button(
            self.resources_frame,
            text="excel_formato.xlsx",
            command=lambda: os.startfile(
                filepath=resolve_route('assets/excel_formato.xlsx')
            )
        )
        excel_button.pack(padx=5, pady=5)

        return excel_button
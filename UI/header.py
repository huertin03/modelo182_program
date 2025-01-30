from tkinter import ttk


class Header:
    def __init__(self, root):
        self.root = root
        self.header = self.crear_header()

    def crear_header(self):
        frame = ttk.Frame(self.root)
        frame.grid(row=0, column=0, columnspan=2)

        title = "Importación masiva de registros del modelo 182"
        title_label = ttk.Label(frame, text=title, font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, padx=20, pady=10, sticky="w")

        description = "Herramienta para generar un fichero de texto con registros del modelo 182 a partir de un archivo Excel."
        description_label = ttk.Label(frame, text=description)
        description_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")

        return frame

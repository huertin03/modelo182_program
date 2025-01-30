from tkinter import ttk

from UI.header import Header
from UI.home import Home


class GUI:
    def __init__(self, root):
        self.root = root
        self.header = Header(root)

        self.notebook = ttk.Notebook(root)
        self.notebook.grid(row=1, column=0, columnspan=2, sticky="nsew")

        self.home_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.home_tab, text="Inicio")
        self.home = Home(self.home_tab)

        self.resources_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.resources_tab, text="Recursos")





    def start(self):
        self.root.mainloop()

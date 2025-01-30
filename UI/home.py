import os
from idlelib.debugger_r import frametable
from tkinter import ttk, StringVar, Button, filedialog, Toplevel

from utils.scritpts import convert_excel_to_182


class Home:
    def __init__(self, root):
        self.root = root

        self.input_route_file = StringVar()
        self.xlsx_file_input = self.create_file_input()

        self.output_file_name = StringVar()
        self.output_file_name.set("fichero.182")
        self.output_file_name_input = self.create_file_name_input()

        self.convert_button = ttk.Button(root, text="Convertir", command=self.convert_excel_to_182)
        self.convert_button.grid(row=2, column=0, padx=20, pady=10)


    def create_file_input(self):
        frame = ttk.Frame(self.root)
        frame.grid(row=0, column=0, padx=20, pady=10)

        label = ttk.Label(frame, text="Ruta del archivo Excel:")
        label.grid(row=0, column=0, padx=5, sticky="w")
        xlsx_file_entry = ttk.Entry(frame, textvariable=self.input_route_file)
        xlsx_file_entry.grid(row=0, column=1, padx=5, sticky="ew")

        xlsx_file_entry.bind("<Button-1>", self.open_file_dialog)

        return frame


    def open_file_dialog(self, event):
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo Excel",
            filetypes=(("Excel files", "*.xlsx"),)
        )
        self.input_route_file.set(file_path)


    def create_file_name_input(self):
        frame = ttk.Frame(self.root)
        frame.grid(row=1, column=0, padx=20, pady=10)

        label = ttk.Label(frame, text="Nombre del fichero de salida:")
        label.grid(row=0, column=0, padx=5, sticky="w")
        output_file_name_entry = ttk.Entry(frame, textvariable=self.output_file_name)
        output_file_name_entry.grid(row=0, column=1, padx=5, sticky="ew")

        return frame


    def convert_excel_to_182(self):
        input_file = self.input_route_file.get()
        output_file = os.path.join(os.path.expanduser("~"), "Downloads", self.output_file_name.get())
        message = convert_excel_to_182(input_file, output_file)

        self.show_message(message)

    def show_message(self, message):
        modal = Toplevel(self.root)
        modal.title("Resultado de la conversión")
        modal.geometry("400x200")
        modal.transient(self.root)
        modal.grab_set()

        message_label = ttk.Label(modal, text=message)
        message_label.pack(padx=20, pady=20)

        close_button = Button(modal, text="OK", command=modal.destroy)
        close_button.pack(pady=10)

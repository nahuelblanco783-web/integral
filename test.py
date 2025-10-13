import customtkinter as ctk
from CTkTable import CTkTable

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.geometry("600x400")
root.title("CTkTable - Selección de fila")

data = [
    ["ID", "Nombre", "Edad", "País"],
    ["1", "Ana", "25", "España"],
    ["2", "Luis", "30", "México"],
    ["3", "Sofía", "27", "Argentina"],
    ["4", "Carlos", "35", "Chile"],
]

def fila_seleccionada(info):
    print(info)  # Primero imprimimos todo para ver la estructura

    print(table.get_row(info["row"]))

table = CTkTable(master=root, values=data, command=fila_seleccionada)
table.pack(padx=20, pady=20, expand=True, fill="both")

root.mainloop()

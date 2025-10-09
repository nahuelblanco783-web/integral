# main.py
import customtkinter as ctk
from gui.login_window import LoginWindow

if __name__ == "__main__":
    app = ctk.CTk()  # Raíz principal (solo una vez)
    login = LoginWindow(master=app)
    login.mainloop()
    
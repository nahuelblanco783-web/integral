from typing import Optional, Tuple, Any, List
import customtkinter as ctk
from CTkSeparator import CTkSeparator
from PIL import Image

class MainWindow(ctk.CTk):
    """Ventana principal de la aplicación."""

    def __init__(self, fg_color: Optional[str | Tuple[str, str]] = "white", user=List[Any], **kwargs: Any) -> None:
        super().__init__(fg_color=fg_color, **kwargs)
        self.user = user

        self.after(0, lambda: self.state('zoomed'))
        self.title("Integral Comunicaciones")
        self.root_width = int(self.winfo_screenwidth())
        self.root_height = int(self.winfo_screenheight())
        self.geometry(f"{self.root_width}x{self.root_height}")

        print(user)

        self.create_menu()

    def create_menu(self) -> None:
        """Crea la barra de menú."""
        self.menu = ctk.CTkFrame(
            self, 
            width=self.root_width, 
            height=50,
            corner_radius=0,
            fg_color="#242423")
        self.menu.pack(side="top", fill="x")


        self.menu.grid_columnconfigure(9, weight=1) 


        self.inicio_button = ctk.CTkButton(
            self.menu, 
            text="INICIO",
            height=35,
            width=0,
            fg_color="#242423",
            hover_color="#4E4E4E",
            text_color="white",
            font=('Lato Light', 20),
            corner_radius=0,
            cursor="hand2",)
        self.inicio_button.grid(row=0, column=0, padx=(25,0),pady=7)

        CTkSeparator(
            self.menu, 
            orientation="vertical", 
            length=35, 
            fg_color="white",
            line_weight=2
        ).grid(row=0, column=1, padx=25)

        self.clientes_button = ctk.CTkButton(
            self.menu, 
            text="CLIENTES",
            height=35,
            width=0,
            fg_color="#242423",
            hover_color="#4E4E4E",
            text_color="white",
            font=('Lato Light', 20),
            corner_radius=0,
            cursor="hand2",)
        self.clientes_button.grid(row=0, column=2)

        CTkSeparator(
            self.menu, 
            orientation="vertical", 
            length=35, 
            fg_color="white",
            line_weight=2
        ).grid(row=0, column=3, padx=25)

        self.empleados_button = ctk.CTkButton(
            self.menu, 
            text="EMPLEADOS",
            height=35,
            width=0,
            fg_color="#242423",
            hover_color="#4E4E4E",
            text_color="white",
            font=('Lato Light', 20),
            corner_radius=0,
            cursor="hand2",)
        self.empleados_button.grid(row=0, column=4)

        CTkSeparator(
            self.menu, 
            orientation="vertical", 
            length=35, 
            fg_color="white",
            line_weight=2
        ).grid(row=0, column=5, padx=25)

        self.soporte_button = ctk.CTkButton(
            self.menu, 
            text="SOPORTE",
            height=35,
            width=0,
            fg_color="#242423",
            hover_color="#4E4E4E",
            text_color="white",
            font=('Lato Light', 20),
            corner_radius=0,
            cursor="hand2",)
        self.soporte_button.grid(row=0, column=6)

        CTkSeparator(
            self.menu, 
            orientation="vertical", 
            length=35, 
            fg_color="white",
            line_weight=2
        ).grid(row=0, column=7, padx=25)

        self.pago_button = ctk.CTkButton(
            self.menu, 
            text="PAGO",
            height=35,
            width=0,
            fg_color="#242423",
            hover_color="#4E4E4E",
            text_color="white",
            font=('Lato Light', 20),
            corner_radius=0,
            cursor="hand2",)
        self.pago_button.grid(row=0, column=8)

        self.account_button = ctk.CTkButton(
            self.menu, 
            text=str(self.user[2]).upper(),
            height=35,
            width=0,
            fg_color="#242423",
            hover_color="#4E4E4E",
            text_color="white",
            font=('Lato Light', 20),
            corner_radius=0,
            cursor="hand2",)
        self.account_button.grid(row=0, column=9, sticky="e", padx=0)

        self.log_out_image=ctk.CTkImage(
            light_image=Image.open("gui\\images\\log_out.png"),
            dark_image=Image.open("gui\\images\\log_out.png"),
            size=(30,25)
        )
        self.log_out_button = ctk.CTkButton(
            self.menu, 
            text="",
            height=35,
            width=0,
            fg_color="#242423",
            hover_color="#4E4E4E",
            text_color="white",
            font=('Lato Light', 20),
            corner_radius=0,
            cursor="hand2",
            image=self.log_out_image,)
        self.log_out_button.grid(row=0, column=10, padx=25)


if __name__ == "__main__":
    app = MainWindow(user=(1, '12345678', 'juan perez', 'juanperez@gmail.com', '123456', 'pisculichi 34', 'secretario', 'Secretaria', '2020-06-23', 'activo', 0, 'hola123'))
    app.mainloop()
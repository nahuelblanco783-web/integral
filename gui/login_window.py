from typing import Optional, Tuple, Any
import customtkinter as ctk
from CTkSeparator import CTkSeparator
from PIL import Image
from CTkMessagebox import CTkMessagebox

from db.gestor_campos import GestorCampos
GestorCamposInstance = GestorCampos()

class LoginWindow(ctk.CTk):
    """Ventana de logeo de empleados."""

    def __init__(self, fg_color: Optional[str | Tuple[str, str]] = None, **kwargs: Any) -> None:
        super().__init__(fg_color=fg_color, **kwargs)

        self.title("Log In - Integral Comunicaciones")
        self.root_width = int(self.winfo_screenwidth() / 1.5)
        self.root_height = int(self.winfo_screenheight() / 1.5)
        self.geometry(f"{self.root_width}x{self.root_height}")

        # Configurar grid principal 2 columnas iguales
        self.grid_columnconfigure(0, weight=1, uniform="a")
        self.grid_columnconfigure(1, weight=1, uniform="a")
        self.grid_rowconfigure(0, weight=1)

        self.login_frame()
        self.right_frame()

    def login_frame(self) -> None:
        """Frame izquierdo donde ingresar los datos"""
        self.login_frame = ctk.CTkFrame(
            master=self,
            corner_radius=0,
            border_width=0,
            fg_color="#E57819"
        )
        self.login_frame.grid(row=0, column=0, sticky="nsew")
        self.login_frame.grid_columnconfigure(0, weight=1)

        # Widgets
        ctk.CTkLabel(
            master=self.login_frame,
            text='Welcome Back',
            font=('Malgun Gothic', 28, 'bold'),
            text_color='white'
        ).grid(row=0, column=0, padx=25, pady=(100, 0), sticky="w")

        CTkSeparator(
            master=self.login_frame,
            length=(self.root_width / 2) - 50,
            line_weight=2,
            dashes=1,
            fg_color='white'
        ).grid(row=1, column=0, padx=25, pady=(25, 0), sticky="w")

        ctk.CTkLabel(
            master=self.login_frame,
            text='DNI',
            font=('Malgun Gothic', 16, 'bold'),
            text_color='white'
        ).grid(row=2, column=0, padx=32, pady=(25, 0), sticky="w")

        self.dni_entry = ctk.CTkEntry(
            master=self.login_frame,
            placeholder_text='Ingrese el DNI...',
            placeholder_text_color='#D9D9D9',
            corner_radius=10,
            border_width=0,
            height=35,
            fg_color='#55473E'
        )
        self.dni_entry.grid(row=3, column=0, padx=25, pady=(5, 0), sticky="we")

        ctk.CTkLabel(
            master=self.login_frame,
            text='Contraseña',
            font=('Malgun Gothic', 16, 'bold'),
            text_color='white'
        ).grid(row=4, column=0, padx=32, pady=(25, 0), sticky="w")

        self.contrasena_entry = ctk.CTkEntry(
            master=self.login_frame,
            placeholder_text='Ingrese la contraseña...',
            placeholder_text_color='#D9D9D9',
            corner_radius=10,
            border_width=0,
            height=35,
            fg_color='#55473E',
            show='*'  # opcional: oculta contraseña
        )
        self.contrasena_entry.grid(row=5, column=0, padx=25, pady=(5, 0), sticky="we")

        self.sign_up_button = ctk.CTkButton(
            master=self.login_frame,
            text='Sign Up',
            text_color='white',
            corner_radius=10,
            border_width=0,
            height=35,
            fg_color='#3F3229',
            hover_color='#55473E',
            command=self.verify_login
        )
        self.sign_up_button.grid(row=6, column=0, padx=25, pady=(50, 0), sticky="we")

        # Espaciador al final
        self.login_frame.grid_rowconfigure(7, weight=1)

    def right_frame(self) -> None:
        """Frame derecho donde mostrar información o imagen"""
        self.right_frame = ctk.CTkFrame(
            master=self,
            corner_radius=0,
            border_width=0,
            fg_color="#55473E"
        )
        self.right_frame.grid(row=0, column=1, sticky="nsew")
        self.right_frame.grid_columnconfigure(0, weight=1)

        integral_image = ctk.CTkImage(
            light_image=Image.open("gui\\images\\integral_logo.png"),
            dark_image=Image.open("gui\\images\\integral_logo.png"),
            size=(40, 40)
        )

        ctk.CTkLabel(
            master=self.right_frame,
            image=integral_image,
            text='  Integral Comunicaciones SRL',
            font=('Malgun Gothic', 22, 'normal'),
            compound='left'
        ).grid(row=0, column=0, padx=25, pady=(100, 0), sticky="nw")

        ctk.CTkLabel(
            master=self.right_frame,
            text='"Conectando personas,\nsimplificando comunicaciones."',
            font=('Lato Light', 28, 'italic'),
            text_color='white',
            justify='left',
        ).grid(row=1, column=0, padx=25, pady=(80,0), sticky="nw")

        # Espaciador al final
        self.right_frame.grid_rowconfigure(1, weight=1)

    def verify_login(self) -> bool:
        """Verifica las credenciales ingresadas. Retorna True si son válidas, False si no."""
        dni = self.dni_entry.get()
        contrasena = self.contrasena_entry.get()
        
        empleado = GestorCamposInstance.read(
            table="empleado",
            where={"dni": dni, "contrasena": contrasena}
        )
        if empleado:
            self.quit()
            self.destroy()
            from gui.main_window import MainWindow
            main_app = MainWindow(user=empleado[0])  # Pasa los datos del empleado a la ventana principal
            main_app.mainloop()  # Abre la ventana principal
            return True
        else:
            CTkMessagebox(
                title="Error de autenticación",
                message="DNI o contraseña incorrectos. Por favor, intente nuevamente.",
                icon="cancel"
            )
            return False
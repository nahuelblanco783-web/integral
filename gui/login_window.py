from typing import Optional, Tuple, Any
import customtkinter as ctk
from CTkSeparator import CTkSeparator
from PIL import Image


class LoginWindow(ctk.CTk):
    """Ventana de logeo de empleados."""

    def __init__(self, fg_color: Optional[str | Tuple[str, str]] = None, **kwargs: Any) -> None:
        super().__init__(fg_color=fg_color, **kwargs)

        self.title("Integral Comunicaciones")
        self.root_width = int(self.winfo_screenwidth() / 1.5)
        self.root_height = int(self.winfo_screenheight() / 1.5)
        self.geometry(f"{self.root_width}x{self.root_height}")
        
        self.login_frame()
        self.right_frame()
    
    def login_frame(self) -> None:
        """Frame izquierdo donde ingresar los datos"""
        self.login_frame = ctk.CTkFrame(
            master=self,
            width=self.root_width / 2,
            height=self.root_height,
            corner_radius=0,
            border_width=0,
            fg_color="#E57819"
        )
        self.login_frame.pack(side='left')
        self.login_frame.pack_propagate(False)
        
        ctk.CTkLabel(
            master=self.login_frame,
            text='Welcome Back',
            font=('Malgun Gothic', 28, 'bold'),
            text_color='white'
        ).pack(padx=(25,0), pady=(100,0), anchor='nw')
        
        separator = CTkSeparator(
            master=self.login_frame,
            length=(self.root_width/2)-50,
            line_weight=2,
            dashes=1,
            fg_color='white'
        )
        separator.pack(padx=(25,0), pady=(25,0), anchor='nw')
        
        ctk.CTkLabel(
            master=self.login_frame,
            text='DNI',
            font=('Malgun Gothic', 16, 'bold'),
            text_color='white'
        ).pack(padx=(32,0), pady=(25,0), anchor='nw')
        
        self.dni_entry = ctk.CTkEntry(
            master=self.login_frame,
            width=(self.root_width/2)-50,
            placeholder_text = 'Ingrese el DNI...',
            placeholder_text_color='#D9D9D9',
            corner_radius=10,
            border_width = 0,
            height=35,
            fg_color='#55473E'
        )
        self.dni_entry.pack(padx=(25,0), pady=(5,0), anchor='nw')
        
        ctk.CTkLabel(
            master=self.login_frame,
            text='Contraseña',
            font=('Malgun Gothic', 16, 'bold'),
            text_color='white'
        ).pack(padx=(32,0), pady=(25,0), anchor='nw')
        
        self.contrasena_entry = ctk.CTkEntry(
            master=self.login_frame,
            width=(self.root_width/2)-50,
            placeholder_text = 'Ingrese la contraseña...',
            placeholder_text_color='#D9D9D9',
            corner_radius=10,
            border_width = 0,
            height=35,
            fg_color='#55473E'
        )
        self.contrasena_entry.pack(padx=(25,0), pady=(5,0), anchor='nw')
        
        self.sign_up_button = ctk.CTkButton(
            master=self.login_frame,
            text='Sign Up',
            text_color='white',
            corner_radius=10,
            border_width=0,
            height=35,
            width=(self.root_width/2)-50,
            fg_color='#3F3229'
        )
        self.sign_up_button.pack(padx=(25,0),pady=(50,0), anchor='nw')
        
    def right_frame(self) -> None:
        """Frame izquierdo donde ingresar los datos"""
        self.right_frame = ctk.CTkFrame(
            master=self,
            width=self.root_width / 2,
            height=self.root_height,
            corner_radius=0,
            border_width=0,
            fg_color="#55473E"
        )
        self.right_frame.pack(side='right')
        self.right_frame.pack_propagate(False)
        
        integral_image = ctk.CTkImage(
            light_image=Image.open("C://Users//pasantia//Documents//integral//gui//images//integral_logo.png"),
            dark_image=Image.open("C://Users//pasantia//Documents//integral//gui//images//integral_logo.png"),
            size=(30, 30))
        
        ctk.CTkLabel(
            master=self.right_frame,
            image=integral_image,
            text='Integral Comunicaciones SRL',
            font=('Malgun Gothic', 20, 'normal'),
            compound='left'    
        ).pack(padx=(25, 0), pady=(100, 0), anchor='nw')
        
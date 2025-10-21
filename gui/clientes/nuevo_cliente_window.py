import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

from db.gestor_campos import GestorCampos

from datetime import datetime

GestorCamposInstance = GestorCampos()

class NuevoCliente(ctk.CTkToplevel):
    """Toplevel para crear un nuevo cliente"""
    def __init__(self, fg_color="white", **kwargs):
        super().__init__(fg_color=fg_color, **kwargs)
        
        self.attributes('-topmost', True)
        
        self.configure(width=800, height=600)
        self.resizable(0, 0)
        self.title('Ingresar nuevo cliente')
        
        self.dni_entry = ctk.CTkEntry(
            master=self,
            width=150,
            height=40,
            corner_radius=0,
            fg_color='#D9D9D9',
            placeholder_text='Ingrese el DNI...',
            border_width=0,
            text_color='black',
            placeholder_text_color='black'
        )
        self.dni_entry.grid(row=0,column=0, padx=(50,25), pady=(50, 25))
        
        self.nombre_entry = ctk.CTkEntry(
            master=self,
            width=150,
            height=40,
            corner_radius=0,
            fg_color='#D9D9D9',
            placeholder_text='Ingrese el Nombre...',
            border_width=0,
            text_color='black',
            placeholder_text_color='black'
        )
        self.nombre_entry.grid(row=0,column=1, padx=(25,50), pady=(50, 25))
        
        self.email_entry = ctk.CTkEntry(
            master=self,
            width=150,
            height=40,
            corner_radius=0,
            fg_color='#D9D9D9',
            placeholder_text='Ingrese el Email...',
            border_width=0,
            text_color='black',
            placeholder_text_color='black'
        )
        self.email_entry.grid(row=1,column=0, padx=(50,25), pady=(0, 25))
        
        self.telefono_entry = ctk.CTkEntry(
            master=self,
            width=150,
            height=40,
            corner_radius=0,
            fg_color='#D9D9D9',
            placeholder_text='Ingrese el Telefono...',
            border_width=0,
            text_color='black',
            placeholder_text_color='black'
        )
        self.telefono_entry.grid(row=1,column=1, padx=(25,50), pady=(0, 25))
        
        self.direccion_entry = ctk.CTkEntry(
            master=self,
            width=150,
            height=40,
            corner_radius=0,
            fg_color='#D9D9D9',
            placeholder_text='Ingrese la Dirección...',
            border_width=0,
            text_color='black',
            placeholder_text_color='black'
        )
        self.direccion_entry.grid(row=2,column=0, padx=(50,25), pady=(0, 50))
        
        self.aceptar_boton = ctk.CTkButton(
            master=self,
            text='Aceptar',
            corner_radius=0,
            border_width=0,
            width=150,
            height=40,
            fg_color='#E57819',
            hover_color='orange',
            command=self.aceptar_cliente
        )
        self.aceptar_boton.grid(row=2, column=1, padx=(25,50), pady=(0, 50))
    
    def aceptar_cliente(self):
        fecha_actual = datetime.now().strftime("%Y-%m-%d")

        self.datos_cliente = [
            self.dni_entry.get(),
            self.nombre_entry.get(),
            self.email_entry.get(),
            self.telefono_entry.get(),
            self.direccion_entry.get(),
            fecha_actual,
            'activo'
        ]

        for i in range(len(self.datos_cliente)):
            if not self.datos_cliente[i]:
                CTkMessagebox(
                    master=self,
                    title='Error',
                    message='No pueden haber campos vacíos, vuelva a ingresar',
                    option_1='Aceptar'
                )
                break

        bandera_cliente=GestorCamposInstance.create(
            'cliente',
            values=self.datos_cliente
        )
        
        if bandera_cliente:
            self.cliente_aceptado_aviso=CTkMessagebox(
                master=self,
                title='Información',
                message='El cliente ha sido ingresado exitosamente',
                option_1='Aceptar',
                icon='info'
            )
            if self.cliente_aceptado_aviso.get() == 'Aceptar':
                self.destroy()            
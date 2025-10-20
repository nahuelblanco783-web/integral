# nuevo_equipo_window.py
import customtkinter as ctk
from db.gestor_campos import GestorCampos
from CTkMessagebox import CTkMessagebox

class NuevoEquipo(ctk.CTkToplevel):
    """Toplevel para crear un nuevo equipo"""
    
    def __init__(self, fg_color="white", **kwargs):
        super().__init__(fg_color=fg_color, **kwargs)
        
        self.attributes('-topmost', True)
        self.configure(width=800, height=600)
        self.resizable(0, 0)
        self.title('Ingresar nuevo equipo')
        
        # Instancia del gestor
        self.gestor_campos = GestorCampos()
        self.campos_equipo = self.gestor_campos.get_campos("equipos")[1:]  # Excluir ID
        
        self._crear_interfaz()
    
    def _crear_interfaz(self):
        """Crea la interfaz de forma dinámica basada en los campos de la tabla"""
        self.entries = {}
        
        for i, campo in enumerate(self.campos_equipo):
            row = i // 2
            col = i % 2
            
            # Label
            ctk.CTkLabel(
                master=self,
                text=f"{campo}:",
                font=("Lato Light", 16),
                text_color="black"
            ).grid(row=row*2, column=col, padx=(50,25), pady=(25,0) if row == 0 else (15,0), sticky="w")
            
            # Entry
            entry = ctk.CTkEntry(
                master=self,
                width=150,
                height=40,
                corner_radius=0,
                fg_color='#D9D9D9',
                placeholder_text=f'Ingrese {campo.lower()}...',
                border_width=0,
                text_color='black',
                placeholder_text_color='black'
            )
            entry.grid(row=row*2+1, column=col, padx=(50,25) if col == 0 else (25,50), 
                      pady=(5,25) if i == len(self.campos_equipo)-1 else (5,0))
            
            self.entries[campo] = entry
        
        # Botón Aceptar
        self.aceptar_boton = ctk.CTkButton(
            master=self,
            text='Aceptar',
            corner_radius=0,
            border_width=0,
            width=150,
            height=40,
            fg_color='#E57819',
            hover_color='orange',
            command=self.aceptar_equipo
        )
        # Colocar el botón en la posición adecuada
        total_rows = ((len(self.campos_equipo) - 1) // 2) * 2 + 2
        self.aceptar_boton.grid(row=total_rows, column=1, padx=(25,50), pady=(0, 25))
    
    def aceptar_equipo(self):
        """Guarda el nuevo equipo en la base de datos"""
        try:
            # Obtener valores de los campos
            valores = [entry.get() for entry in self.entries.values()]
            
            # Insertar en la base de datos
            bandera_equipo = self.gestor_campos.create('equipos', valores)
            
            if bandera_equipo:
                CTkMessagebox(
                    master=self,
                    title='Información',
                    message='El equipo ha sido ingresado exitosamente',
                    option_1='Aceptar',
                    icon='info'
                )
                self.destroy()
            else:
                CTkMessagebox(
                    master=self,
                    title='Error',
                    message='Error al ingresar el equipo',
                    icon='cancel'
                )
                
        except Exception as e:
            CTkMessagebox(
                master=self,
                title='Error',
                message=f'Error: {str(e)}',
                icon='cancel'
            )
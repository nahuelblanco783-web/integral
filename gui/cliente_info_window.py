import customtkinter as ctk
from db.gestor_campos import GestorCampos
from typing import List
ctk.set_appearance_mode("light")

class InfoCliente(ctk.CTkToplevel):
    """ Toplevel para mostrar toda la información del cliente y las acciones posibles (modificar, dar de baja y/o ver cuenta)"""
    
    def __init__(self, fg_color="white", cliente=None, **kwargs):
        super().__init__(fg_color=fg_color, **kwargs)
        self.cliente = cliente
    
        self.attributes('-topmost', True)
        
        self.configure(width=800, height=600)
        self.resizable(0, 0)
        self.title('Información de '+self.cliente[1])

        #Instancias y variables
        self.gestor_campos = GestorCampos()
        self.campos_cliente = self.gestor_campos.get_campos("cliente")
        print(self.campos_cliente)

        #Crear la interfaz
        self.info_cliente_frame()
        self.acciones_cliente_frame()

    # ---------------------------------------------------------------------
    # --------------------- CREACIÓN DE INTERFAZ --------------------------
    # ---------------------------------------------------------------------
    def info_cliente_frame(self):
        #Frame
        self.info_frame=ctk.CTkFrame(
            master=self,
            border_width=0,
            corner_radius=0
        )
        self.info_frame.grid(row=0, column=0, pady=25, padx=25)

        # Obtenemos los campos y excluimos Id Cliente
        self.campos_cliente = self.gestor_campos.get_campos("cliente")[1:]  # excluimos 'Id Cliente'
        self.info_frame.stringvars = {}  # Diccionario para guardar los StringVar

        for idx, campo in enumerate(self.campos_cliente):
            row = idx // 2 * 2       # Cada 2 campos, bajamos 2 filas
            col = idx % 2            # columna 0 o 1

            # Label
            ctk.CTkLabel(
                master=self.info_frame,
                text=f"{campo}:",
                font=("Lato Light", 20)
            ).grid(row=row, column=col, padx=25, pady=(25 if row == 0 else 10,0), sticky='w')

            # StringVar
            sv = ctk.StringVar(master=self)
            self.info_frame.stringvars[campo] = sv

            # Entry
            value = self.cliente[idx] if idx < len(self.cliente) else ""
            entry = ctk.CTkEntry(
                master=self.info_frame,
                width=150,
                height=45,
                border_width=0,
                corner_radius=0,
                placeholder_text=value,
                state='disabled',
                textvariable=sv
            )
            # Margen inferior si es el último entry
            entry_pady = (5,25) if idx == len(self.campos_cliente)-1 else (5,0)
            entry.grid(row=row+1, column=col, padx=25, pady=entry_pady, sticky='w')

            sv.set(value)

            # Botón "Aceptar" al final
            if idx == len(self.campos_cliente)-1:
                boton_aceptar = ctk.CTkButton(
                    master=self.info_frame,
                    text="Aceptar",
                    width=150,
                    height=45,
                    corner_radius=0,
                    command=self.destroy,
                    state='disabled'
                )
                # Lo colocamos a la derecha del último Entry
                boton_aceptar.grid(row=row+1, column=col+1, padx=25, pady=(5,25), sticky='w')

    def acciones_cliente_frame(self):
        self.acciones_frame=ctk.CTkFrame(
            master=self,
            border_width=0,
            corner_radius=0
        )
        self.acciones_frame.grid(row=0, column=1, pady=25, padx=(0, 25), sticky='ns')
        
        #Botones
        self.acciones_frame.modificar_btn = ctk.CTkButton(
            master=self.acciones_frame,
            width=150,
            height=45,
            text='Editar',
            corner_radius=0
        )
        self.acciones_frame.modificar_btn.grid(row=0,column=0, pady=(58,0), padx=25)

        self.acciones_frame.detalle_cuenta_btn = ctk.CTkButton(
            master=self.acciones_frame,
            width=150,
            height=45,
            text='Ver cuenta',
            corner_radius=0
        )
        self.acciones_frame.detalle_cuenta_btn.grid(row=1,column=0, pady=(43,0), padx=25)

        self.acciones_frame.detalle_contratos_btn = ctk.CTkButton(
            master=self.acciones_frame,
            width=150,
            height=45,
            text='Ver Contratos',
            corner_radius=0
        )
        self.acciones_frame.detalle_contratos_btn.grid(row=2,column=0, pady=(43,0), padx=25)

        self.acciones_frame.eliminar_btn = ctk.CTkButton(
            master=self.acciones_frame,
            width=150,
            height=45,
            text='Dar de baja',
            corner_radius=0
        )
        self.acciones_frame.eliminar_btn.grid(row=3,column=0, pady=(43,0), padx=25)

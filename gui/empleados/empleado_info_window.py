import customtkinter as ctk
from db.gestor_campos import GestorCampos
from CTkMessagebox import CTkMessagebox
ctk.set_appearance_mode("light")

class InfoEmpleado(ctk.CTkToplevel):
    """ Toplevel para mostrar toda la información del empleado y las acciones posibles (modificar, dar de baja y/o ver cuenta)"""
    
    def __init__(self, fg_color="white", empleado=None, row_empleado=None, table=None, **kwargs):
        super().__init__(fg_color=fg_color, **kwargs)
        self.empleado = empleado
        self.row_empleado = row_empleado
        self.table = table
    
        self.attributes('-topmost', True)
        
        self.configure(width=800, height=600)
        self.resizable(0, 0)
        self.title('Información de '+self.empleado[1])

        #Instancias y variables
        self.gestor_campos = GestorCampos()
        self.campos_empleado = self.gestor_campos.get_campos("empleado")
        
        #Obtener id del empleado
        self.id_empleado = self.gestor_campos.read(
            'empleado',
            {'dni':self.empleado[0]}
        )
        self.id_empleado = self.id_empleado[0][0]

        #Crear la interfaz
        self.info_empleado_frame()
        self.acciones_empleado_frame()

    # ---------------------------------------------------------------------
    # --------------------- CREACIÓN DE INTERFAZ --------------------------
    # ---------------------------------------------------------------------
    def info_empleado_frame(self):
        #Frame
        self.info_frame=ctk.CTkFrame(
            master=self,
            border_width=0,
            corner_radius=0
        )
        self.info_frame.grid(row=0, column=0, pady=25, padx=25)

        self.campos_empleado = self.gestor_campos.get_campos("empleado")[1:]  
        self.info_frame.stringvars = {}  
        self.entries_list = []

        for idx, campo in enumerate(self.campos_empleado):
            row = idx // 2 * 2       
            col = idx % 2            

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
            value = self.empleado[idx] if idx < len(self.empleado) else ""
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
            entry_pady = (5,25) if idx == len(self.campos_empleado)-1 else (5,0)
            entry.grid(row=row+1, column=col, padx=25, pady=entry_pady, sticky='w')

            self.entries_list.append(entry)

            sv.set(value)

            # Botón "Aceptar" al final
            if idx == len(self.campos_empleado)-1:
                self.boton_aceptar = ctk.CTkButton(
                    master=self.info_frame,
                    text="Aceptar",
                    width=150,
                    height=45,
                    corner_radius=0,
                    command=self.aceptar_cambios,
                    state='disabled'
                )
                # Lo colocamos a la derecha del último Entry
                self.boton_aceptar.grid(row=row+1, column=col+1, padx=25, pady=(5,25), sticky='w')

    def acciones_empleado_frame(self):
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
            corner_radius=0,
            command=self.editar_empleado
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

    # ---------------------------------------------------------------------
    # --------------------- FUNCIONALIDAD ---------------------------------
    # ---------------------------------------------------------------------
    def editar_empleado(self):
        #Habilitar entries y el boton
        for entry in self.entries_list:
            entry.configure(state='normal')
        self.boton_aceptar.configure(state='normal')
    
    def aceptar_cambios(self):
        #Crear lista de los nuevos campos del empleado
        self.empleado_actualizado=[]
        for entry in self.entries_list:
            self.empleado_actualizado.append(entry.get())
        self.empleado_actualizado.append(self.id_empleado)

        #Actualizar empleado
        bandera_empleado=self.gestor_campos.update(
            table='empleado',
            values=self.empleado_actualizado
        )

        #deshabilitar botones
        for entry in self.entries_list:
            entry.configure(state='disabled')
        self.boton_aceptar.configure(state='disabled')

        #verificar messagebox
        if bandera_empleado:
            self.aceptar_msg=CTkMessagebox(
                master=self,
                title='Información',
                message='empleado actualizado exitosamente',
                option_1='Aceptar'
            )
            self.empleado_actualizado.pop()
            
            #Actualizar fila de la tabla
            for i, campo in enumerate(self.empleado_actualizado):
                self.table.insert(row=self.row_empleado, column=i, value=campo)
        
        else:
            self.error_msg=CTkMessagebox(
                master=self,
                title='Error',
                message='Error actualizando al empleado',
                option_1='Aceptar',
                icon='error'
            )

    def ver_cuenta(self):
        pass

    def ver_contratos(self):
        pass

    def dar_de_baja(self):
        pass
# equipo_info_window.py
import customtkinter as ctk
from db.gestor_campos import GestorCampos
from CTkMessagebox import CTkMessagebox
from typing import List


class InfoEquipo(ctk.CTkToplevel):
    """Toplevel para mostrar toda la información del equipo y las acciones posibles"""
    
    def __init__(self, fg_color="white", equipo=None, **kwargs):
        super().__init__(fg_color=fg_color, **kwargs)
        self.equipo = equipo
    
        self.attributes('-topmost', True)
        self.configure(width=800, height=600)
        self.resizable(0, 0)
        self.title('Información de Equipo')

        # Instancias y variables
        self.gestor_campos = GestorCampos()
        self.campos_equipo = self.gestor_campos.get_campos("equipos")
        self.editando = False

        # Crear la interfaz
        self.info_equipo_frame()
        self.acciones_equipo_frame()

    def info_equipo_frame(self):
        """Frame para mostrar la información del equipo"""
        self.info_frame = ctk.CTkFrame(
            master=self,
            border_width=0,
            corner_radius=0
        )
        self.info_frame.grid(row=0, column=0, pady=25, padx=25)

        # Excluir ID del equipo
        self.campos_visibles = self.campos_equipo[1:]
        self.info_frame.stringvars = {}

        for idx, campo in enumerate(self.campos_visibles):
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
            value = self.equipo[idx + 1] if idx + 1 < len(self.equipo) else ""  # +1 para saltar ID
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
            entry_pady = (5,25) if idx == len(self.campos_visibles)-1 else (5,0)
            entry.grid(row=row+1, column=col, padx=25, pady=entry_pady, sticky='w')

            sv.set(value)

            # Botón "Aceptar" al final
            if idx == len(self.campos_visibles)-1:
                self.boton_aceptar = ctk.CTkButton(
                    master=self.info_frame,
                    text="Aceptar",
                    width=150,
                    height=45,
                    corner_radius=0,
                    command=self.destroy,
                    state='normal'
                )
                self.boton_aceptar.grid(row=row+1, column=col+1, padx=25, pady=(5,25), sticky='w')

    def acciones_equipo_frame(self):
        """Frame para los botones de acciones"""
        self.acciones_frame = ctk.CTkFrame(
            master=self,
            border_width=0,
            corner_radius=0
        )
        self.acciones_frame.grid(row=0, column=1, pady=25, padx=(0, 25), sticky='ns')
        
        # Botones
        self.acciones_frame.modificar_btn = ctk.CTkButton(
            master=self.acciones_frame,
            width=150,
            height=45,
            text='Editar',
            corner_radius=0,
            command=self.toggle_edicion
        )
        self.acciones_frame.modificar_btn.grid(row=0, column=0, pady=(58,0), padx=25)

        self.acciones_frame.eliminar_btn = ctk.CTkButton(
            master=self.acciones_frame,
            width=150,
            height=45,
            text='Eliminar',
            corner_radius=0,
            fg_color="#D93535",
            hover_color="#B32B2B",
            command=self.eliminar_equipo
        )
        self.acciones_frame.eliminar_btn.grid(row=1, column=0, pady=(43,0), padx=25)

    def toggle_edicion(self):
        """Alterna entre modo edición y visualización"""
        self.editando = not self.editando
        
        # Cambiar estado de los entries
        for widget in self.info_frame.winfo_children():
            if isinstance(widget, ctk.CTkEntry):
                widget.configure(state='normal' if self.editando else 'disabled')
        
        # Cambiar texto del botón
        if self.editando:
            self.acciones_frame.modificar_btn.configure(text='Guardar', fg_color='#2E8B57')
            self.boton_aceptar.configure(state='disabled')
        else:
            self.acciones_frame.modificar_btn.configure(text='Editar', fg_color='#3B8ED0')
            self.boton_aceptar.configure(state='normal')
            self.guardar_cambios()

    def guardar_cambios(self):
        """Guarda los cambios realizados en el equipo"""
        try:
            # Obtener nuevos valores
            nuevos_valores = []
            for campo in self.campos_visibles:
                nuevos_valores.append(self.info_frame.stringvars[campo].get())
            
            # Agregar ID del equipo al final (para el WHERE en el UPDATE)
            nuevos_valores.append(self.equipo[0])  # ID del equipo
            
            # Actualizar en base de datos
            if self.gestor_campos.update('equipos', nuevos_valores):
                CTkMessagebox(
                    master=self,
                    title='Éxito',
                    message='Equipo actualizado correctamente',
                    icon='info'
                )
            else:
                CTkMessagebox(
                    master=self,
                    title='Error',
                    message='Error al actualizar el equipo',
                    icon='cancel'
                )
                
        except Exception as e:
            CTkMessagebox(
                master=self,
                title='Error',
                message=f'Error al guardar cambios: {str(e)}',
                icon='cancel'
            )

    def eliminar_equipo(self):
        """Elimina el equipo de la base de datos"""
        confirmar = CTkMessagebox(
            master=self,
            title='Confirmar eliminación',
            message='¿Estás seguro de que deseas eliminar este equipo?',
            option_1='Cancelar',
            option_2='Eliminar',
            icon='warning'
        )
        
        if confirmar.get() == 'Eliminar':
            try:
                if self.gestor_campos.delete('equipos', {'id_equipo': self.equipo[0]}):
                    CTkMessagebox(
                        master=self,
                        title='Éxito',
                        message='Equipo eliminado correctamente',
                        icon='info'
                    )
                    self.destroy()
                else:
                    CTkMessagebox(
                        master=self,
                        title='Error',
                        message='Error al eliminar el equipo',
                        icon='cancel'
                    )
            except Exception as e:
                CTkMessagebox(
                    master=self,
                    title='Error',
                    message=f'Error al eliminar: {str(e)}',
                    icon='cancel'
                )
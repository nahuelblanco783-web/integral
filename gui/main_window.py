from gui.menu_frame import MenuFrame
from gui.inicio_frame import InicioFrame
from gui.clientes.clientes_frame import ClientesFrame
from gui.empleados.empleados_frame import EmpleadosFrame
from gui.equipos.equipos_frame import EquiposFrame

from db.gestor_campos import GestorCampos

import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

GestorCamposInstance = GestorCampos()

class MainWindow(ctk.CTkToplevel):
    def __init__(self, fg_color="white", user=None, **kwargs):
        super().__init__(fg_color=fg_color, **kwargs)
        self.user = user
        self.permisos_user = GestorCamposInstance.read(
            table='rol_base',
            where={"id_rol_base": user[-1]}
        )[0]

        self.after(0, lambda: self.state('zoomed'))
        self.title("Integral Comunicaciones")
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # --- Callbacks de navegación ---
        callbacks = {
            "inicio": self.show_inicio,
            "clientes": self.show_clientes,
            # "soporte": self.show_soporte,
            "empleados": self.show_empleados,
            # "pago": self.show_pago,
            "equipos": self.show_equipos,
            "log_out": self.log_out
        }

        self.menu = MenuFrame(self, user=self.user, permisos_user=self.permisos_user, callbacks=callbacks)

        # Aquí crearías los frames de contenido
        self.current_frame = None
        self.show_inicio()

    def show_inicio(self):
        self._show_frame(InicioFrame, user=self.user)

    def show_clientes(self):
        self._show_frame(ClientesFrame, user=self.user)
    
    def show_empleados(self):
        self._show_frame(EmpleadosFrame, user=self.user)
    
    def show_equipos(self):
        self._show_frame(EquiposFrame, user=self.user)

    # ... métodos similares para soporte, empleados, etc.

    def _show_frame(self, frame_class, *args, **kwargs):
        if self.current_frame is not None:
            self.current_frame.pack_forget()
        self.current_frame = frame_class(self, *args, **kwargs)  # args van al constructor del frame
        self.current_frame.pack(fill="both", expand=True)

    def log_out(self):
        confirmar_salir = CTkMessagebox(
            master=self,
            title='',
            message='¿Deseas salir?',
            option_1='Cancelar',
            option_2='Salir',
            icon='question'
        )

        if confirmar_salir.get() == 'Salir':
            self.destroy()  # Cierra solo esta ventana

            # Abrir nuevamente LoginWindow usando la misma raíz
            from gui.login_window import LoginWindow
            login_app = LoginWindow(master=self.master)
            login_app.focus()

    def on_close(self):
        self.destroy()    # destruye la ventana
        import sys
        sys.exit()

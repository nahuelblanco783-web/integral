import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from datetime import datetime

from db.gestor_campos import GestorCampos


class NuevoEmpleado(ctk.CTkToplevel):
    """Toplevel para crear un nuevo empleado."""

    def __init__(self, fg_color="white", **kwargs):
        super().__init__(fg_color=fg_color, **kwargs)

        self.attributes("-topmost", True)

        self.resizable(False, False)
        self.title("Ingresar nuevo empleado")

        # Instancias y datos auxiliares
        self.gestor_campos = GestorCampos()
        self.roles_disponibles = self._cargar_roles()
        self.estados_disponibles = ["activo", "inactivo"]

        # Widgets
        self._crear_formulario()

    # ---------------------------------------------------------------------
    # Construcción de interfaz
    # ---------------------------------------------------------------------
    def _crear_formulario(self):
        padding_x = (50, 25)
        padding_y = (40, 25)

        self.dni_entry = self._crear_entry("Ingrese el DNI...", 0, 0, padding_x, (50, 25))
        self.nombre_entry = self._crear_entry("Ingrese el Nombre...", 0, 1, (25, 50), (50, 25))
        self.email_entry = self._crear_entry("Ingrese el Email...", 1, 0, padding_x, padding_y)
        self.telefono_entry = self._crear_entry("Ingrese el Teléfono...", 1, 1, (25, 50), padding_y)
        self.direccion_entry = self._crear_entry("Ingrese la Dirección...", 2, 0, padding_x, padding_y)
        self.zona_entry = self._crear_entry("Ingrese la Zona de trabajo...", 2, 1, (25, 50), padding_y)
        self.contrasena_entry = self._crear_entry("Ingrese la Contraseña...", 3, 0, padding_x, padding_y, show="*")

        # Fecha de ingreso sugerida (hoy)
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        self.fecha_entry = self._crear_entry("Fecha de ingreso (AAAA-MM-DD)...", 3, 1, (25, 50), padding_y)
        self.fecha_entry.insert(0, fecha_actual)

        # Estado
        ctk.CTkLabel(
            master=self,
            text="Estado:",
            text_color="black"
        ).grid(row=4, column=0, padx=padding_x, pady=(10, 5), sticky="w")

        self.estado_menu = ctk.CTkOptionMenu(
            master=self,
            values=self.estados_disponibles,
            width=150,
            height=40,
            fg_color="#D9D9D9",
            button_color="#E57819",
            text_color="black"
        )
        self.estado_menu.set(self.estados_disponibles[0])
        self.estado_menu.grid(row=5, column=0, padx=padding_x, pady=(0, 25), sticky="w")

        # Rol Base
        ctk.CTkLabel(
            master=self,
            text="Rol base:",
            text_color="black"
        ).grid(row=4, column=1, padx=(25, 50), pady=(10, 5), sticky="w")

        if self.roles_disponibles:
            opciones_roles = [rol["nombre"] for rol in self.roles_disponibles]
        else:
            opciones_roles = ["Sin roles cargados"]

        self.rol_menu = ctk.CTkOptionMenu(
            master=self,
            values=opciones_roles,
            width=150,
            height=40,
            fg_color="#D9D9D9",
            button_color="#E57819",
            text_color="black"
        )
        self.rol_menu.set(opciones_roles[0])
        self.rol_menu.grid(row=5, column=1, padx=(25, 50), pady=(0, 25), sticky="w")

        # Botón aceptar
        self.aceptar_boton = ctk.CTkButton(
            master=self,
            text="Aceptar",
            corner_radius=0,
            border_width=0,
            width=150,
            height=45,
            fg_color="#E57819",
            hover_color="orange",
            command=self._aceptar_empleado
        )
        self.aceptar_boton.grid(row=6, column=0, columnspan=2, pady=(0, 40))

    def _crear_entry(self, placeholder, row, column, padx, pady, show=""):
        entry = ctk.CTkEntry(
            master=self,
            width=150,
            height=40,
            corner_radius=0,
            fg_color="#D9D9D9",
            placeholder_text=placeholder,
            border_width=0,
            text_color="black",
            placeholder_text_color="black",
            show=show
        )
        entry.grid(row=row, column=column, padx=padx, pady=pady, sticky="w")
        return entry

    # ---------------------------------------------------------------------
    # Funcionalidad
    # ---------------------------------------------------------------------
    def _cargar_roles(self):
        """Obtiene los roles disponibles para poblar el OptionMenu."""
        try:
            registros = self.gestor_campos.read(table="rol_base", where={})
            return [
                {"id": fila[0], "nombre": fila[1]}
                for fila in registros
            ]
        except Exception as exc:
            CTkMessagebox(
                master=self,
                title="Advertencia",
                message=f"No se pudieron cargar los roles: {exc}",
                icon="warning",
                option_1="Aceptar"
            )
            return []

    def _aceptar_empleado(self):
        """Valida los campos y crea un nuevo empleado."""
        fecha_ingreso = self.fecha_entry.get().strip() or datetime.now().strftime("%Y-%m-%d")
        ultimo_acceso = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        estado = self.estado_menu.get()

        rol_seleccionado = self.rol_menu.get()
        rol_id = None
        for rol in self.roles_disponibles:
            if rol["nombre"] == rol_seleccionado:
                rol_id = rol["id"]
                break

        datos_empleado = [
            self.dni_entry.get().strip(),
            self.nombre_entry.get().strip(),
            self.email_entry.get().strip(),
            self.telefono_entry.get().strip(),
            self.direccion_entry.get().strip(),
            self.zona_entry.get().strip(),
            fecha_ingreso,
            estado,
            ultimo_acceso,
            self.contrasena_entry.get().strip(),
            rol_id if rol_id is not None else ""
        ]

        if any(not dato for dato in datos_empleado):
            CTkMessagebox(
                master=self,
                title="Error",
                message="No pueden haber campos vacíos. Revisa la información ingresada.",
                option_1="Aceptar",
                icon="cancel"
            )
            return

        bandera_empleado = self.gestor_campos.create(
            "empleado",
            values=datos_empleado
        )

        if bandera_empleado:
            aviso = CTkMessagebox(
                master=self,
                title="Información",
                message="El empleado ha sido ingresado exitosamente.",
                option_1="Aceptar",
                icon="info"
            )
            if aviso.get() == "Aceptar":
                self.destroy()
        else:
            CTkMessagebox(
                master=self,
                title="Error",
                message="Hubo un problema al crear el empleado. Intenta nuevamente.",
                option_1="Aceptar",
                icon="cancel"
            )
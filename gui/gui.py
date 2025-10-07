import customtkinter as ctk
from CTkMenuBar import CTkMenuBar, CustomDropdownMenu
from CTkTable import CTkTable
from CTkXYFrame import CTkXYFrame
from typing import Any, Optional, Tuple, List, cast

# Importamos directamente las clases en lugar de los módulos
from db.gestor_campos import DatabaseManager as CamposDBManager
from db.gestor_tablas import DatabaseManager as TablasDBManager
from db.db_utils import sql

# Configuración inicial de la UI
ctk.set_appearance_mode("light")

# Instancias de gestores de base de datos
gestor_tablas = TablasDBManager()
gestor_campos = CamposDBManager()


class Root(ctk.CTk):
    """Ventana principal de la aplicación."""

    def __init__(self, fg_color: Optional[str | Tuple[str, str]] = None, **kwargs: Any) -> None:
        super().__init__(fg_color, **kwargs)

        self.title("Chinnesse people")
        self.root_width = 800
        self.root_height = 600
        self.geometry(f"{self.root_width}x{self.root_height}")

        self.main_frame: ctk.CTkFrame | None = None

        self._create_menu()
        self._create_main_frame()

    # -------------------
    # Sección de Menú
    # -------------------
    def _create_menu(self) -> None:
        """Crea la barra de menús principal."""
        menu = CTkMenuBar(
            master=self,
            bg_color="white",
            height=25,
            width=10,
            padx=0,
            pady=0,
        )

        # --- Menú Empleados ---
        employee_menu_button = menu.add_cascade(
            text="Empleados",
            hover_color="#dbdbdb",
            corner_radius=0,
            postcommand=self._show_employees_frame,
        )
        employee_menu_button.configure(width=100, anchor="center")

        # --- Menú Clientes ---
        customer_menu_button = menu.add_cascade(
            text="Clientes",
            hover_color="#dbdbdb",
            corner_radius=0,
            postcommand=self._show_customers_frame,
        )
        customer_menu_button.configure(width=100, anchor="center")

        # --- Menú Mesa de ayuda ---
        help_table_menu_button = menu.add_cascade(
            text="Mesa de ayuda",
            hover_color="#dbdbdb",
            corner_radius=0,
        )
        help_table_menu_button.configure(width=100, anchor="center")

        CustomDropdownMenu(
            widget=help_table_menu_button,
            corner_radius=0,
            border_width=0,
            separator_color="#adadad",
        )

    # -------------------
    # Sección de Frames
    # -------------------
    def _create_main_frame(self) -> None:
        """Crea el frame principal donde se mostrarán los contenidos."""
        self.main_frame = ctk.CTkFrame(master=self, fg_color="#ebebeb", corner_radius=0)
        self.main_frame.pack(fill="both", expand=True, padx=0, pady=0)

    def _show_customers_frame(self) -> None:
        """Crea y muestra el frame con la tabla de clientes y un frame superior con botón de agregar cliente."""
        # Limpiar frame principal
        if self.main_frame is not None:
            widgets: List[Any] = cast(List[Any], self.main_frame.winfo_children())
            for widget in widgets:
                widget.destroy()

        if not self.main_frame:
            return

        # Frame superior dinámico (no scrollable) para acciones
        action_frame = ctk.CTkFrame(master=self.main_frame, fg_color="#f5f5f5", corner_radius=8)
        action_frame.pack(fill="x", padx=25, pady=(25, 0))

        def on_add_user() -> None:
            añadir_usuario(self, gestor_campos)

        add_button = ctk.CTkButton(
            master=action_frame,
            text="Añadir usuario",
            command=on_add_user,
            corner_radius=6,
            fg_color="#4caf50",
            hover_color="#388e3c",
            text_color="white",
            width=160,
            height=32,
            font=("Arial", 14, "bold"),
        )
        add_button.pack(side="left", padx=10, pady=10)

        # Frame principal scrollable para la tabla y filtros
        customer_xy_frame = CTkXYFrame(
            master=self.main_frame,
            width=self.root_width - 20,
            height=self.root_height - 500,
        )
        customer_xy_frame.pack(fill="both", expand=True, padx=25, pady=(5,25), side="bottom")

        # -------------------
        # Función auxiliar
        # -------------------
        def show_customer_details(cliente: tuple[Any, ...]) -> None:
            """Abre una ventana emergente con los detalles del cliente."""
            print("Abriendo detalle de cliente...")
            top = ctk.CTkToplevel(self)
            top.title("Detalle del cliente")
            top.geometry("400x300")
            top.lift()
            top.grab_set()

            with sql.connect(gestor_campos.nombre_bd) as conn:
                cursor = conn.cursor()
                cursor.execute("PRAGMA table_info(clientes)")
                campos: list[str] = [row[1] for row in cursor.fetchall()]

            for campo, valor in zip(campos, cliente):
                label = ctk.CTkLabel(top, text=f"{campo}: {valor}")
                label.pack(anchor="w", padx=20, pady=5)

        # -------------------
        # Lógica principal
        # -------------------
        clientes: list[tuple[Any, ...]] = gestor_campos.read("clientes")

        with sql.connect(gestor_campos.nombre_bd) as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA table_info(clientes)")
            campos: list[str] = [row[1] for row in cursor.fetchall()]

        campos_sin_id: list[str] = [c for c in campos if c != "id"]
        idxs_sin_id: list[int] = [i for i, c in enumerate(campos) if c != "id"]

        # Entradas de filtrado alineadas con la tabla
        entry_frame = ctk.CTkFrame(customer_xy_frame, corner_radius=0, border_width=0)
        entry_frame.pack(fill="x", padx=5, pady=(5,0))

        entry_widgets: list[ctk.CTkEntry] = []
        num_columns = len(campos_sin_id)
        # Calcula el ancho de cada entry para que coincida con la tabla
        table_total_width = customer_xy_frame.winfo_width() if customer_xy_frame.winfo_width() > 0 else self.root_width - 60
        _entry_width = int(table_total_width / num_columns) + 100 # Ajuste de padding

        for i, campo in enumerate(campos_sin_id):
            placeholder = campo.replace("_", " ").capitalize() + "..."
            entry = ctk.CTkEntry(
            entry_frame,
            placeholder_text=placeholder,
            placeholder_text_color="gray",
            corner_radius=0,
            border_width=0,
            font=("Arial", 13),
            )
            if i == 0:
                entry.grid(row=0, column=i, padx=(0,1), pady=0, sticky="nsew")
            elif i == num_columns - 1:
                entry.grid(row=0, column=i, padx=(1,0), pady=0, sticky="nsew")
            else:
                entry.grid(row=0, column=i, padx=1, pady=0, sticky="nsew")
            entry_widgets.append(entry)

            def on_key_release(_event: Any) -> None:
                update_table()
            entry.bind("<KeyRelease>", on_key_release)

        # Asegura que las columnas del frame ocupen el mismo espacio que la tabla
        for i in range(num_columns):
            entry_frame.grid_columnconfigure(i, weight=1)

        # Tabla dinámica
        table_widget: CTkTable | None = None

        def update_table(*_args: Any) -> None:
            nonlocal table_widget

            filtros = [entry.get().strip().lower() for entry in entry_widgets]

            filtered_clientes = [
                cliente
                for cliente in clientes
                if all(f == "" or f in str(cliente[i]).lower() for f, i in zip(filtros, idxs_sin_id))
            ]

            values: list[list[Any]] = [[cliente[i] for i in idxs_sin_id] for cliente in filtered_clientes]

            if table_widget is not None:
                table_widget.destroy()

            def cell_command(event: dict[str, Any]) -> None:
                print(f"Celda clickeada, valor: {event}")
                row: int = event.get("row", 0)
                if 0 <= row < len(filtered_clientes):
                    show_customer_details(filtered_clientes[row])

            table_widget = CTkTable(
                master=customer_xy_frame,
                row=len(values),
                column=len(campos_sin_id),
                values=values,
                command=cell_command,
                corner_radius=0,
            )
            table_widget.pack(expand=True, fill="both", padx=5, pady=(1,5))

        update_table()
        customer_xy_frame.update_idletasks()

    
    def _show_employees_frame(self) -> None:
        """Crea y muestra el frame con la tabla de empleados y un frame superior con botón de agregar usuario."""
        # Limpiar frame principal
        if self.main_frame is not None:
            widgets: List[Any] = cast(List[Any], self.main_frame.winfo_children())
            for widget in widgets:
                widget.destroy()

        if not self.main_frame:
            return

        # Frame superior dinámico (no scrollable) para acciones
        action_frame = ctk.CTkFrame(master=self.main_frame, fg_color="#f5f5f5", corner_radius=8)
        action_frame.pack(fill="x", padx=25, pady=(25, 0))

        def on_add_user() -> None:
            añadir_usuario(self, gestor_campos)

        add_button = ctk.CTkButton(
            master=action_frame,
            text="Añadir usuario",
            command=on_add_user,
            corner_radius=6,
            fg_color="#4caf50",
            hover_color="#388e3c",
            text_color="white",
            width=160,
            height=32,
            font=("Arial", 14, "bold"),
        )
        add_button.pack(side="left", padx=10, pady=10)

        # Frame principal scrollable para la tabla y filtros
        employee_xy_frame = CTkXYFrame(
            master=self.main_frame,
            width=self.root_width - 20,
            height=self.root_height - 500,
        )
        employee_xy_frame.pack(fill="both", expand=True, padx=25, pady=(5,25), side="bottom")

        # Función auxiliar para mostrar detalles
        def show_employee_details(empleado: tuple[Any, ...]) -> None:
            top = ctk.CTkToplevel(self)
            top.title("Detalle del empleado")
            top.geometry("400x300")
            top.lift()
            top.grab_set()
            with sql.connect(gestor_campos.nombre_bd) as conn:
                cursor = conn.cursor()
                cursor.execute("PRAGMA table_info(empleados)")
                campos: list[str] = [row[1] for row in cursor.fetchall()]
            for campo, valor in zip(campos, empleado):
                label = ctk.CTkLabel(top, text=f"{campo}: {valor}")
                label.pack(anchor="w", padx=20, pady=5)

        # Lógica principal
        empleados: list[tuple[Any, ...]] = gestor_campos.read("empleados")
        with sql.connect(gestor_campos.nombre_bd) as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA table_info(empleados)")
            campos: list[str] = [row[1] for row in cursor.fetchall()]
        campos_sin_id: list[str] = [c for c in campos if c != "id"]
        idxs_sin_id: list[int] = [i for i, c in enumerate(campos) if c != "id"]

        # Entradas de filtrado alineadas con la tabla
        entry_frame = ctk.CTkFrame(employee_xy_frame, corner_radius=0, border_width=0)
        entry_frame.pack(fill="x", padx=5, pady=(5,0))

        entry_widgets: list[ctk.CTkEntry] = []
        num_columns = len(campos_sin_id)
        table_total_width = employee_xy_frame.winfo_width() if employee_xy_frame.winfo_width() > 0 else self.root_width - 60
        _entry_width = int(table_total_width / num_columns) + 100

        for i, campo in enumerate(campos_sin_id):
            placeholder = campo.replace("_", " ").capitalize() + "..."
            entry = ctk.CTkEntry(
                entry_frame,
                placeholder_text=placeholder,
                placeholder_text_color="gray",
                corner_radius=0,
                border_width=0,
                font=("Arial", 13),
            )
            if i == 0:
                entry.grid(row=0, column=i, padx=(0,1), pady=0, sticky="nsew")
            elif i == num_columns - 1:
                entry.grid(row=0, column=i, padx=(1,0), pady=0, sticky="nsew")
            else:
                entry.grid(row=0, column=i, padx=1, pady=0, sticky="nsew")
            entry_widgets.append(entry)
            def on_key_release(_event: Any) -> None:
                update_table()
            entry.bind("<KeyRelease>", on_key_release)
        for i in range(num_columns):
            entry_frame.grid_columnconfigure(i, weight=1)

        # Tabla dinámica
        table_widget: CTkTable | None = None
        def update_table(*_args: Any) -> None:
            nonlocal table_widget
            filtros = [entry.get().strip().lower() for entry in entry_widgets]
            filtered_empleados = [
                empleado
                for empleado in empleados
                if all(f == "" or f in str(empleado[i]).lower() for f, i in zip(filtros, idxs_sin_id))
            ]
            values: list[list[Any]] = [[empleado[i] for i in idxs_sin_id] for empleado in filtered_empleados]
            if table_widget is not None:
                table_widget.destroy()
            def cell_command(event: dict[str, Any]) -> None:
                row: int = event.get("row", 0)
                if 0 <= row < len(filtered_empleados):
                    show_employee_details(filtered_empleados[row])
            table_widget = CTkTable(
                master=employee_xy_frame,
                row=len(values),
                column=len(campos_sin_id),
                values=values,
                command=cell_command,
                corner_radius=0,
            )
            table_widget.pack(expand=True, fill="both", padx=5, pady=(1,5))
        update_table()
        employee_xy_frame.update_idletasks()

    # -------------------
    # Sección de Funciones Aux.
    # -------------------
    
def añadir_usuario(parent: ctk.CTk, gestor_campos: CamposDBManager) -> None:
    """Abre una ventana para añadir un usuario (empleado o cliente) con campos dinámicos."""
    win = ctk.CTkToplevel(parent)
    win.title("Añadir usuario")
    win.geometry("420x500")
    win.lift()
    win.grab_set()

    tipo_var = ctk.StringVar(value="cliente")

    tipo_label = ctk.CTkLabel(win, text="¿Qué tipo de usuario deseas ingresar?", font=("Arial", 13, "bold"))
    tipo_label.pack(anchor="w", padx=10, pady=(15,0))
    tipo_combo = ctk.CTkComboBox(win, values=["cliente", "empleado"], variable=tipo_var)
    tipo_combo.pack(fill="x", padx=10, pady=(0,10))

    # Frame scrollable para los campos
    campos_scroll = CTkXYFrame(win, width=380, height=340)
    campos_scroll.pack(fill="both", expand=True, padx=10, pady=10)

    campos_frame = ctk.CTkFrame(campos_scroll)
    campos_frame.pack(fill="both", expand=True)

    entry_vars: dict[str, ctk.StringVar] = {}

    def get_campos(tipo: str) -> list[str]:
        tabla = "empleados" if tipo == "empleado" else "clientes"
        with sql.connect(gestor_campos.nombre_bd) as conn:
            cursor = conn.cursor()
            cursor.execute(f"PRAGMA table_info({tabla})")
            campos = [row[1] for row in cursor.fetchall() if row[1] != "id"]
        return campos

    def render_campos(*_args: Any) -> None:
        for widget in campos_frame.winfo_children(): # pyright: ignore[reportUnknownVariableType]
            widget.destroy()
        campos = get_campos(tipo_var.get())
        entry_vars.clear()
        for campo in campos:
            label = ctk.CTkLabel(campos_frame, text=campo.capitalize()+":", font=("Arial", 12))
            label.pack(anchor="w", padx=5, pady=(8,0))
            var = ctk.StringVar()
            entry = ctk.CTkEntry(campos_frame, textvariable=var, placeholder_text=campo.capitalize())
            entry.pack(fill="x", padx=5, pady=(0,8))
            entry_vars[campo] = var

    tipo_combo.configure(command=render_campos)
    render_campos()

    def guardar_usuario() -> None:
        tabla = "empleados" if tipo_var.get() == "empleado" else "clientes"
        datos = {campo: var.get() for campo, var in entry_vars.items()}
        gestor_campos.create(tabla, datos)
        win.destroy()
        # Opcional: podrías refrescar la tabla principal aquí

    guardar_btn = ctk.CTkButton(win, text="Guardar", command=guardar_usuario, fg_color="#2196f3", text_color="white")
    guardar_btn.pack(pady=15)


if __name__ == "__main__":
    ventana = Root()
    ventana.mainloop()

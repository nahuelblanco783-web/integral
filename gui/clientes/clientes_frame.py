import threading
import customtkinter as ctk
from PIL import Image
from CTkXYFrame import CTkXYFrame
from CTkTable import CTkTable
from db.gestor_campos import GestorCampos
from gui.clientes.cliente_info_window import InfoCliente


class ClientesFrame(ctk.CTkFrame):
    """Frame principal para la gestión de clientes."""

    def __init__(self, master, user, **kwargs):
        super().__init__(master, **kwargs)
        self.user = user
        self.configure(corner_radius=0, border_width=0, fg_color="#D9D9D9")
        self.pack(fill="both", expand=True)

        # Instancias y variables
        self.gestor_campos = GestorCampos()
        self.campos_cliente = self.gestor_campos.get_campos("cliente")
        self._filtro_timer = None
        self._fila_popup_actual = None
        self._datos_fila_popup = None

        # Construcción de la interfaz
        self._crear_submenu()
        self._crear_contenido()

    # ---------------------------------------------------------------------
    # --------------------- CREACIÓN DE INTERFAZ --------------------------
    # ---------------------------------------------------------------------

    def _crear_submenu(self):
        """Crea el encabezado superior con logo y botón."""
        self.columnconfigure(0, weight=1)

        self.sub_menu = ctk.CTkFrame(self, corner_radius=0, fg_color="#A4A4A4", height=80)
        self.sub_menu.grid(row=0, column=0, sticky="ew")

        # Logo
        logo_img = ctk.CTkImage(
            light_image=Image.open("gui/images/integral.png"),
            dark_image=Image.open("gui/images/integral.png"),
            size=(45, 60)
        )
        ctk.CTkLabel(
            self.sub_menu,
            text="  Integral Comunicaciones SRL",
            text_color="white",
            font=("Lato Light", 36),
            image=logo_img,
            compound="left"
        ).grid(row=0, column=0, padx=(25, 0), pady=5)

        # Botón "Nuevo cliente"
        self.sub_menu.columnconfigure(2, weight=1)
        nuevo_btn = ctk.CTkButton(
            self.sub_menu,
            text="+",
            font=("Lato Light", 24, "bold"),
            width=40,
            height=40,
            corner_radius=0,
            fg_color="#D9D9D9",
            hover_color="#BFBFBF",
            text_color="white",
            command=self.nuevo_cliente
        )
        nuevo_btn.grid(row=0, column=2, padx=(0, 25), pady=5, sticky="e")

    def _crear_contenido(self):
        """Crea el cuerpo principal con los campos de búsqueda y la tabla."""
        self.rowconfigure(1, weight=1)

        self.content_frame = CTkXYFrame(self, corner_radius=0, fg_color="white")
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=25, pady=25)

        self._crear_filtros()
        self._crear_tabla()

    def _crear_filtros(self):
        """Crea los campos de búsqueda (entries)."""
        self.entries = {}

        entries_frame = ctk.CTkFrame(self.content_frame, corner_radius=0, fg_color="black", height=45)
        entries_frame.grid(row=0, column=0, sticky="ew")

        for i, campo in enumerate(self.campos_cliente[1:]):  # Excluye el ID
            entry = ctk.CTkEntry(
                entries_frame,
                font=("Lato Light", 16),
                width=150,
                height=50,
                border_width=0,
                corner_radius=0,
                placeholder_text=f"{campo}...",
                fg_color="white",
                text_color="black",
                placeholder_text_color="gray"
            )
            padx = (0, 1) if i == 0 else (1, 0) if i == len(self.campos_cliente[1:]) - 1 else 1
            entry.grid(row=0, column=i, padx=padx, pady=0)
            entry.bind("<KeyRelease>", self._filtrar_tabla)
            self.entries[campo] = entry

    def _crear_tabla(self):
        """Crea la tabla de datos de clientes."""
        table_frame = ctk.CTkFrame(self.content_frame, corner_radius=0, fg_color="black", height=45)
        table_frame.grid(row=1, column=0, sticky="nsew")

        # Cargar datos
        raw_data = self.gestor_campos.read(table="cliente", where={})
        self._datos_originales = [list(row[1:]) for row in raw_data]  # Excluir id_cliente
        self._datos_filtrados = list(self._datos_originales)

        rows = len(self._datos_originales)
        cols = len(self.campos_cliente) - 1

        self.table = CTkTable(
            master=table_frame,
            values=self._datos_originales,
            column=cols,
            row=rows,
            width=150,
            height=50,
            corner_radius=0,
            border_width=0,
            colors=["#D9D9D9", "white"],
            text_color="black",
            pady=1,
            cursor="hand2",
            command=self.info_cliente
        )
        self.table.grid(row=0, column=0, sticky="nsew")

    # ---------------------------------------------------------------------
    # --------------------- FUNCIONALIDAD --------------------------------
    # ---------------------------------------------------------------------

    def _filtrar_tabla(self, event=None):
        """Activa el filtrado con retardo (debounce)."""
        if self._filtro_timer and self._filtro_timer.is_alive():
            self._filtro_timer.cancel()

        self._filtro_timer = threading.Timer(0.25, self._ejecutar_filtrado)
        self._filtro_timer.start()

    def _ejecutar_filtrado(self):
        """Aplica los filtros ingresados en los campos."""
        filtros = [e.get().strip().lower() for e in self.entries.values()]

        if all(not f for f in filtros):
            datos_filtrados = self._datos_originales
        else:
            datos_filtrados = [
                fila for fila in self._datos_originales
                if all(
                    not filtro or str(valor).lower().startswith(filtro)
                    for valor, filtro in zip(fila, filtros)
                )
            ]

        self.after(0, lambda: self._actualizar_tabla(datos_filtrados))

    def _actualizar_tabla(self, nuevos_datos):
        """Actualiza los valores de la tabla."""
        filas_max = len(self._datos_originales)
        cols = len(self.campos_cliente) - 1

        # Rellenar filas vacías si hay menos resultados
        nuevos_datos += [[""] * cols for _ in range(filas_max - len(nuevos_datos))]
        self.table.update_values(nuevos_datos)

    def nuevo_cliente(self):
        """Abre la ventana para crear un nuevo cliente."""
        from gui.clientes.nuevo_cliente_window import NuevoCliente
        NuevoCliente().mainloop()- 

    def info_cliente(self, info):
        """LLama a la clase InfoCliente para mostrar todas las opciones posibles a realizarle."""
        cliente = self.table.get_row(info["row"])
        row_cliente=info["row"]

        info_cliente = InfoCliente(cliente=cliente, table=self.table, row_cliente=row_cliente)
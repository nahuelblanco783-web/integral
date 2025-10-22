import threading
import customtkinter as ctk
from PIL import Image
from CTkXYFrame import CTkXYFrame
from CTkTable import CTkTable
from db.gestor_campos import GestorCampos
from gui.equipos.nuevo_equipo_window import NuevoEquipo
from gui.equipos.equipo_info_window import InfoEquipo
from CTkMessagebox import CTkMessagebox

class EquiposFrame(ctk.CTkFrame):
    """Frame principal para la gestión de equipos."""

    def __init__(self, master, user, **kwargs):
        super().__init__(master, **kwargs)
        self.user = user

        self.configure(corner_radius=0, border_width=0, fg_color="#D9D9D9")
        self.pack(fill="both", expand=True)

        self.gestor_campos = GestorCampos()
        self.tabla_equipos, self.campos_equipo = self._cargar_campos_equipo()
        self.campos_visibles = self.campos_equipo[1:]  # Excluir ID

        # Variables para filtros
        self._filtro_timer = None
        self._datos_originales = []
        self._datos_filtrados = []
        self.entries = {}
        self.comboboxes = {}  # Para los comboboxes
        
        # Identificar columnas especiales
        self.columnas_fecha = [campo for campo in self.campos_visibles 
                               if any(palabra in campo.lower() for palabra in ['fecha', 'date'])]
        self.columnas_estado = [campo for campo in self.campos_visibles 
                                if any(palabra in campo.lower() for palabra in ['estado', 'state', 'status'])]
        
        # Valores posibles para el estado (se detectarán automáticamente)
        self.estados_posibles = ["Todos"]

        self._crear_submenu()
        self._crear_contenido()

    def _cargar_campos_equipo(self):
        for nombre_tabla in ("equipos", "equipo"):
            try:
                campos = self.gestor_campos.get_campos(nombre_tabla)
                if campos:
                    return nombre_tabla, list(campos)
            except Exception:
                continue
        
        # Tabla y campos por defecto si no se encuentra
        return (
            "equipos",
            [
                "id_equipo", "id_cliente", "tipo_equipo", "marca", 
                "modelo", "serie", "fecha_instalacion", "estado"
            ],
        )

    def _crear_submenu(self):
        """Crea el encabezado superior con logo y botón."""
        self.columnconfigure(0, weight=1)

        self.sub_menu = ctk.CTkFrame(self, corner_radius=0, fg_color="#A4A4A4", height=80)
        self.sub_menu.grid(row=0, column=0, sticky="ew")

        logo_img = ctk.CTkImage(
            light_image=Image.open("gui/images/integral.png"),
            dark_image=Image.open("gui/images/integral.png"),
            size=(45, 60),
        )
        ctk.CTkLabel(
            self.sub_menu,
            text="  Integral Comunicaciones SRL",
            text_color="white",
            font=("Lato Light", 36),
            image=logo_img,
            compound="left",
        ).grid(row=0, column=0, padx=(25, 0), pady=5)

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
            command=self.nuevo_equipo,
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
        """Crea los campos de búsqueda con combobox para estado."""
        entries_frame = ctk.CTkFrame(self.content_frame, corner_radius=0, fg_color="black", height=45)
        entries_frame.grid(row=0, column=0, sticky="ew")

        for i, campo in enumerate(self.campos_visibles):
            # Frame para cada columna
            col_frame = ctk.CTkFrame(entries_frame, fg_color="white", corner_radius=0)
            col_frame.grid(row=0, column=i, 
                           padx=(0, 1) if i == 0 else (1, 0) if i == len(self.campos_visibles) - 1 else 1, 
                           pady=0, sticky="nsew")

            # Para columnas de estado, usar combobox
            if campo in self.columnas_estado:
                combobox = ctk.CTkComboBox(
                    col_frame,
                    values=self.estados_posibles,
                    font=("Lato Light", 16),
                    width=150,
                    height=50,
                    border_width=0,
                    corner_radius=0,
                    fg_color="white",
                    text_color="black",
                    dropdown_fg_color="white",
                    dropdown_text_color="black",
                    dropdown_hover_color="#D9D9D9",
                    button_color="#E57819",
                    button_hover_color="#BF5A15"
                )
                combobox.set("Todos")  # Valor por defecto
                combobox.pack(side="left", fill="both", expand=True)
                
                # SOLUCIÓN: Usar command en lugar de bind para respuesta inmediata
                combobox.configure(command=lambda value, c=campo: self._on_combobox_change(c, value))
                self.comboboxes[campo] = combobox
                # También lo guardamos en entries para mantener la estructura
                self.entries[campo] = combobox

            # Para otras columnas (incluyendo fechas), usar entry normal
            else:
                entry = ctk.CTkEntry(
                    col_frame,
                    font=("Lato Light", 16),
                    width=150,
                    height=50,
                    border_width=0,
                    corner_radius=0,
                    placeholder_text=f"{campo}...",
                    fg_color="white",
                    text_color="black",
                    placeholder_text_color="gray",
                )
                entry.pack(side="left", fill="both", expand=True)
                entry.bind("<KeyRelease>", self._filtrar_tabla)
                self.entries[campo] = entry

    def _on_combobox_change(self, campo, value):
        """Maneja el cambio en el combobox y filtra inmediatamente."""
        # Ejecutar filtrado inmediatamente sin timer
        self._ejecutar_filtrado()

    def _crear_tabla(self):
        """Crea la tabla de datos de equipos."""
        table_frame = ctk.CTkFrame(self.content_frame, corner_radius=0, fg_color="black", height=45)
        table_frame.grid(row=1, column=0, sticky="nsew")

        # Cargar datos
        raw_data = self._obtener_registros()
        self._datos_originales = [list(row[1:]) for row in raw_data]  # Excluir ID
        self._datos_filtrados = list(self._datos_originales)

        # Detectar estados únicos automáticamente
        self._detectar_estados_unicos()

        rows = len(self._datos_originales)
        cols = len(self.campos_visibles)

        # Si no hay datos, crear una tabla con una fila vacía
        if rows == 0:
            rows = 1
            valores_tabla = [[""] * cols]
        else:
            valores_tabla = self._datos_originales

        self.table = CTkTable(
            master=table_frame,
            values=valores_tabla,
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
            command=self.info_equipo,
        )
        self.table.grid(row=0, column=0, sticky="nsew")

    def _obtener_registros(self):
        """Devuelve los registros de la tabla de equipos."""
        for nombre_tabla in (self.tabla_equipos, "equipos", "equipo"):
            if not nombre_tabla:
                continue
            try:
                registros = self.gestor_campos.read(table=nombre_tabla, where={})
                if registros is not None:
                    if nombre_tabla != self.tabla_equipos:
                        self.tabla_equipos = nombre_tabla
                    return registros
            except Exception:
                continue
        return []

    def _detectar_estados_unicos(self):
        """Detecta automáticamente los estados únicos de la base de datos."""
        try:
            if not self.columnas_estado:
                return
            
            columna_estado = self.columnas_estado[0]  # Tomar la primera columna de estado
            indice_columna = self.campos_visibles.index(columna_estado)
            
            estados = set()
            for fila in self._datos_originales:
                if len(fila) > indice_columna:
                    estado = str(fila[indice_columna]).strip()
                    if estado:
                        estados.add(estado)
            
            if estados:
                # Ordenar alfabéticamente y agregar "Todos" al principio
                estados_ordenados = sorted(estados)
                self.estados_posibles = ["Todos"] + estados_ordenados
                
                # Actualizar el combobox si existe
                if columna_estado in self.comboboxes:
                    self.comboboxes[columna_estado].configure(values=self.estados_posibles)
            
        except Exception as e:
            print(f"Error detectando estados únicos: {e}")

    def _filtrar_tabla(self, event=None):
        """Activa el filtrado con retardo (debounce)."""
        if self._filtro_timer and self._filtro_timer.is_alive():
            self._filtro_timer.cancel()

        self._filtro_timer = threading.Timer(0.25, self._ejecutar_filtrado)
        self._filtro_timer.start()

    def _ejecutar_filtrado(self):
        """Aplica los filtros ingresados en los campos."""
        filtros = []
        
        # Recoger valores de todos los filtros
        for campo in self.campos_visibles:
            if campo in self.columnas_estado:
                # Para combobox, obtener el valor seleccionado
                valor = self.entries[campo].get()
                # Si es "Todos", no filtrar por este campo
                filtros.append("" if valor == "Todos" else valor.lower())
            else:
                # Para entries, obtener el texto normal
                filtros.append(self.entries[campo].get().strip().lower())

        if all(not f for f in filtros):
            datos_filtrados = self._datos_originales
        else:
            datos_filtrados = []
            for fila in self._datos_originales:
                cumple_filtro = True
                for valor, filtro, campo in zip(fila, filtros, self.campos_visibles):
                    if filtro:
                        valor_str = str(valor).lower()
                        
                        # Para campos de fecha, búsqueda flexible (buscar en cualquier parte)
                        if campo in self.columnas_fecha:
                            if filtro not in valor_str:
                                cumple_filtro = False
                                break
                        # Para campos de estado, comparación exacta (ignorando case)
                        elif campo in self.columnas_estado:
                            if valor_str != filtro:
                                cumple_filtro = False
                                break
                        else:
                            # Para otros campos, mantener búsqueda por inicio
                            if not valor_str.startswith(filtro):
                                cumple_filtro = False
                                break
                if cumple_filtro:
                    datos_filtrados.append(fila)

        self.after(0, lambda: self._actualizar_tabla(datos_filtrados))

    def _actualizar_tabla(self, nuevos_datos):
        """Actualiza los valores de la tabla."""
        filas_max = len(self._datos_originales)
        cols = len(self.campos_visibles)

        # Rellenar filas vacías si hay menos resultados
        nuevos_datos += [[""] * cols for _ in range(filas_max - len(nuevos_datos))]
        self.table.update_values(nuevos_datos)

    def nuevo_equipo(self):
        """Abre la ventana para crear un nuevo equipo."""
        nuevo_equipo_window = NuevoEquipo()
        nuevo_equipo_window.mainloop()

    def info_equipo(self, info):
        """Abre la ventana de información del equipo seleccionado."""
        # Obtener datos completos del equipo (incluyendo ID)
        datos_fila = self.table.get_row(info["row"])
        
        if not datos_fila or all(str(campo).strip() == "" for campo in datos_fila):
            return
        
        # Obtener el ID del equipo de la base de datos
        raw_data = self._obtener_registros()
        equipo_completo = None
        
        for equipo in raw_data:
            # Comparar si los datos coinciden (excluyendo el ID)
            if list(equipo[1:]) == datos_fila:
                equipo_completo = list(equipo)
                break
        
        if equipo_completo:
            info_equipo = InfoEquipo(equipo=equipo_completo)
        else:
            # Si no se encuentra, mostrar mensaje de error
            CTkMessagebox(
                title="Error",
                message="No se pudo cargar la información completa del equipo",
                icon="cancel"
            )
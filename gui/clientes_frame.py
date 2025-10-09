import customtkinter as ctk
from PIL import Image
from CTkXYFrame import CTkXYFrame
from gui.popup_window import CTkFloatingWindow
from db.gestor_campos import GestorCampos
from CTkTable import CTkTable
import threading
GestorCamposInstance = GestorCampos()

class ClientesFrame(ctk.CTkFrame):
    """Frame de los clientes del programa / main window, contenido dinámico según la opción del menú"""
    def __init__(self, master, user, **kwargs):
        super().__init__(master, **kwargs)
        self.user = user
        self.configure(corner_radius=0, border_width=0, fg_color='#D9D9D9')
        self.pack(fill='both', expand=True)
    
        # ---[ Sub Menu ]---
        self.columnconfigure(0, weight=1)
        self.sub_menu = ctk.CTkFrame(
            master=self,
            corner_radius=0,
            border_width=0,
            fg_color='#A4A4A4',
            height=80
        )
        self.sub_menu.grid(row=0, column=0, sticky='ew')

        integral_image = ctk.CTkImage(
            light_image=Image.open("gui\\images\\integral.png"),
            dark_image=Image.open("gui\\images\\integral.png"),
            size=(45, 60)
        )
        ctk.CTkLabel(
            master=self.sub_menu,
            text='  Integral Comunicaciones SRL',
            text_color='white',
            font=('Lato Light', 36),
            image=integral_image,
            compound='left',
        ).grid(row=0, column=0, padx=(25, 0), pady=5)

        self.sub_menu.columnconfigure(1, weight=1)

        self.sub_menu.nuevo_cliente_button = ctk.CTkButton(
            master=self.sub_menu,
            text='+',
            font=('Lato Light', 24, 'bold'),
            width=40,
            height=40,
            corner_radius=0,
            fg_color='#D9D9D9',
            hover_color='#BFBFBF',
            text_color='white',
            command=lambda: print('nuevo cliente')
        )
        self.sub_menu.nuevo_cliente_button.grid(row=0, column=2, padx=(0, 25), pady=5, sticky='e')
        
        # ---[ Content Frame ]---
        self.rowconfigure(1, weight=1)
        self.content_frame = CTkXYFrame(
            master=self,
            corner_radius=0,
            border_width=0,
            fg_color='white',
        )
        self.content_frame.grid(row=1, column=0, sticky='nsew', padx=25, pady=25)

        self.campos_cliente = GestorCamposInstance.get_campos("cliente")

        # ---[ Entries de búsqueda ]---
        self.content_frame.entries_frame = ctk.CTkFrame(
            master=self.content_frame,
            corner_radius=0,
            border_width=0,
            fg_color='black',
            height=45
        )
        self.content_frame.entries_frame.grid(row=0, column=0, sticky='ew', padx=0, pady=0)

        # Diccionario para guardar los entries
        self.entries = {}

        for i, campo in enumerate(self.campos_cliente[1:]):  # Excluyo id_cliente
            entry = ctk.CTkEntry(
                master=self.content_frame.entries_frame,
                font=('Lato Light', 16),
                width=150,
                height=50,
                border_width=0,
                corner_radius=0,
                placeholder_text=f'{campo}...',
                fg_color='white',
                text_color='black',
                placeholder_text_color='gray'
            )
            if i == 0:
                padx = (0, 1)
            elif i == len(self.campos_cliente[1:]) - 1:
                padx = (1, 0)
            else:
                padx = 1
            entry.grid(row=0, column=i, padx=padx, pady=0)
            self.entries[campo] = entry

            # 👇 Vinculamos evento: cuando cambia el texto, actualiza la tabla
            entry.bind("<KeyRelease>", self.filtrar_tabla)

        # ---[ Tabla de datos ]---
        self.content_frame.table_frame = ctk.CTkFrame(
            master=self.content_frame,
            corner_radius=0,
            border_width=0,
            fg_color='black',
            height=45
        )
        self.content_frame.table_frame.grid(row=1, column=0, sticky='nsew')

        self.values_clientes = GestorCamposInstance.read(
            table='cliente',
            where={}
        )
        self.values_clientes = [t[1:] for t in self.values_clientes]
        self.rows_clientes = len(self.values_clientes)
        self.columns_clientes = len(self.campos_cliente) - 1

        # Guardamos los datos originales para filtrar sin tocar la fuente
        self._datos_originales = list(self.values_clientes)

        self.content_frame.table_frame.table = CTkTable(
            master=self.content_frame.table_frame,
            values=self.values_clientes,
            column=self.columns_clientes,
            row=self.rows_clientes,
            width=150,
            height=50,
            corner_radius=0,
            border_width=0,
            colors=['#D9D9D9', 'white'],
            text_color='black',
            pady=1,
            cursor='hand2'
        )
        self.content_frame.table_frame.table.grid(row=0, column=0, sticky='nsew')

        def do_popup(event, frame):
            """ open the popup menu """
            try: frame.popup(event.x_root, event.y_root)
            finally: frame.grab_release()

        self.content_frame.table_frame.table.bind("<Button-3>", lambda event: do_popup(event, self.popup_menu))

        # --- [ Popup Menu ] ---
        self.popup_menu = CTkFloatingWindow(self)

        self.popup_menu.modificar_button = ctk.CTkButton(
            master=self.popup_menu.frame,
            text="Modificar",
            fg_color="transparent",
            text_color='black',
            corner_radius=0,
            hover_color='white',
            command=lambda: print("Modificar cliente")
        )
        self.popup_menu.modificar_button.pack()
        self.popup_menu.dar_de_baja_button = ctk.CTkButton(
            master=self.popup_menu.frame,
            text="Dar de baja",
            fg_color="transparent",
            text_color='black',
            corner_radius=0,
            hover_color='white',
            command=lambda: print("Dar de baja cliente")
        )
        self.popup_menu.dar_de_baja_button.pack()



    # ---[ Método de filtrado dinámico ]---
    def filtrar_tabla(self, event=None):
        """Filtra la tabla después de un pequeño retardo (debounce)."""
        # Cancelar un filtro anterior en curso (si el usuario sigue escribiendo)
        if hasattr(self, "_filtro_timer") and self._filtro_timer.is_alive():
            self._filtro_timer.cancel()

        # Programar el filtrado real después de 250 ms
        self._filtro_timer = threading.Timer(0.25, self._ejecutar_filtrado)
        self._filtro_timer.start()

    def _ejecutar_filtrado(self):
        """Filtrado real (se ejecuta con un pequeño retraso)."""
        filtros = [entry.get().strip().lower() for entry in self.entries.values()]

        if all(f == "" for f in filtros):
            datos_filtrados = self._datos_originales
        else:
            datos_filtrados = []
            for fila in self._datos_originales:
                coincide = True
                for valor, filtro in zip(fila, filtros):
                    if filtro and not str(valor).lower().startswith(filtro):
                        coincide = False
                        break
                if coincide:
                    datos_filtrados.append(fila)

        # Actualizar tabla en el hilo principal (Tkinter no permite hacerlo desde otro)
        self.after(0, lambda: self.actualizar_tabla(datos_filtrados))

    def actualizar_tabla(self, nuevos_datos):
        """Actualiza los valores de la tabla sin recrearla, limpiando las filas sobrantes."""
        filas_max = len(self._datos_originales)
        filas_actuales = len(nuevos_datos)

        # Si hay menos filas, rellena con vacías para evitar errores visuales
        if filas_actuales < filas_max:
            nuevos_datos = nuevos_datos + [[""] * self.columns_clientes for _ in range(filas_max - filas_actuales)]

        # Actualiza solo los valores visibles
        self.content_frame.table_frame.table.update_values(nuevos_datos)
   

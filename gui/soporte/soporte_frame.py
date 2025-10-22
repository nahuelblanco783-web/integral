import customtkinter as ctk
from db.gestor_campos import GestorCampos
from PIL import Image
from CTkMessagebox import CTkMessagebox
import datetime

class SoporteFrame(ctk.CTkFrame):
    """Sistema de soporte moderno e intuitivo - Sin Header"""

    def __init__(self, master, user, **kwargs):
        super().__init__(master, **kwargs)
        self.user = user
        self.configure(corner_radius=0, border_width=0, fg_color="#F5F5F5")
        
        # Instancias
        self.gestor_campos = GestorCampos()
        
        # Variables de estado
        self.ticket_seleccionado = None
        self.tecnico_seleccionado = None
        
        # Colores del tema
        self.colores = {
            "primario": "#E57819",
            "secundario": "#2C3E50",
            "exito": "#27AE60",
            "peligro": "#E74C3C",
            "advertencia": "#F39C12",
            "info": "#3498DB",
            "fondo": "#F5F5F5",
            "card": "#FFFFFF",
            "texto_oscuro": "#2C3E50",
            "texto_claro": "#7F8C8D"
        }
        
        self._crear_interfaz()
        self._cargar_datos()

    def _crear_interfaz(self):
        """Crea la interfaz completa del sistema de soporte."""
        # Solo submenú y contenido principal (sin header)
        self._crear_submenu()
        self._crear_contenido_principal()

    def _crear_submenu(self):
        """Crea el submenú superior al estilo de Equipos."""
        self.sub_menu = ctk.CTkFrame(self, corner_radius=0, fg_color="#A4A4A4", height=80)
        self.sub_menu.pack(fill="x", padx=0, pady=0)
        self.sub_menu.pack_propagate(False)

        # Logo pequeño
        logo_img = ctk.CTkImage(
            light_image=Image.open("gui/images/integral.png"),
            dark_image=Image.open("gui/images/integral.png"),
            size=(35, 45),
        )
        ctk.CTkLabel(
            self.sub_menu,
            text="  Integral Comunicaciones SRL",
            text_color="white",
            font=("Lato Light", 24),
            image=logo_img,
            compound="left",
        ).pack(side="left", padx=(25, 0), pady=5)

        # Espaciador
        self.sub_menu.columnconfigure(1, weight=1)

        # Botones de acción
        botones_frame = ctk.CTkFrame(self.sub_menu, fg_color="transparent")
        botones_frame.pack(side="right", padx=25, pady=5)

        # Botón Actualizar
        ctk.CTkButton(
            botones_frame,
            text="🔄 Actualizar",
            font=("Lato Light", 14),
            width=120,
            height=40,
            fg_color="#D9D9D9",
            hover_color="#BFBFBF",
            text_color="black",
            command=self._actualizar_todo
        ).pack(side="left", padx=(0, 10))

        # Botón Nuevo Ticket
        ctk.CTkButton(
            botones_frame,
            text="➕ Nuevo Ticket",
            font=("Lato Light", 14),
            width=120,
            height=40,
            fg_color="#D9D9D9",
            hover_color="#BFBFBF",
            text_color="black",
            command=self._abrir_nuevo_ticket
        ).pack(side="left")

    def _crear_contenido_principal(self):
        """Crea el contenido principal dividido en dos secciones."""
        main_frame = ctk.CTkFrame(self, fg_color=self.colores["fondo"])
        main_frame.pack(fill="both", expand=True, padx=25, pady=25)

        # Configurar grid 2 columnas
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)

        # Sección izquierda - Técnicos
        self._crear_seccion_tecnicos(main_frame)
        
        # Sección derecha - Tickets
        self._crear_seccion_tickets(main_frame)

    def _crear_seccion_tecnicos(self, parent):
        """Crea la sección de técnicos."""
        tecnicos_frame = ctk.CTkFrame(parent, fg_color=self.colores["card"], corner_radius=12)
        tecnicos_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=0)

        # Título
        ctk.CTkLabel(
            tecnicos_frame,
            text="Empleados Disponibles",
            text_color=self.colores["texto_oscuro"],
            font=("Lato Light", 20, "bold")
        ).pack(pady=20)

        # Filtro y búsqueda
        filtro_frame = ctk.CTkFrame(tecnicos_frame, fg_color="transparent")
        filtro_frame.pack(fill="x", padx=20, pady=(0, 15))

        # ComboBox para filtrar por tipo de empleado
        ctk.CTkLabel(
            filtro_frame,
            text="Tipo:",
            text_color=self.colores["texto_oscuro"],
            font=("Lato Light", 12)
        ).pack(side="left", padx=(0, 10))

        self.filtro_tipo_empleado = ctk.CTkComboBox(
            filtro_frame,
            values=["Todos", "Técnico", "Administrador", "Secretaria"],
            width=140,
            height=35,
            command=self._filtrar_empleados_por_tipo
        )
        self.filtro_tipo_empleado.set("Todos")
        self.filtro_tipo_empleado.pack(side="left", padx=(0, 15))

        # Búsqueda
        self.buscar_tecnico_entry = ctk.CTkEntry(
            filtro_frame,
            placeholder_text="🔍 Buscar...",
            height=35
        )
        self.buscar_tecnico_entry.pack(side="left", fill="x", expand=True)
        self.buscar_tecnico_entry.bind("<KeyRelease>", self._filtrar_tecnicos)

        # Lista de técnicos
        self.tecnicos_scroll = ctk.CTkScrollableFrame(
            tecnicos_frame, 
            fg_color=self.colores["fondo"],
            corner_radius=8
        )
        self.tecnicos_scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def _crear_seccion_tickets(self, parent):
        """Crea la sección de tickets."""
        tickets_frame = ctk.CTkFrame(parent, fg_color=self.colores["card"], corner_radius=12)
        tickets_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=0)

        # Título
        ctk.CTkLabel(
            tickets_frame,
            text="Tickets de Soporte",
            text_color=self.colores["texto_oscuro"],
            font=("Lato Light", 20, "bold")
        ).pack(pady=20)

        # Filtros
        filtros_frame = ctk.CTkFrame(tickets_frame, fg_color="transparent")
        filtros_frame.pack(fill="x", padx=20, pady=(0, 15))

        # Filtro por estado
        ctk.CTkLabel(
            filtros_frame,
            text="Estado:",
            text_color=self.colores["texto_oscuro"],
            font=("Lato Light", 12)
        ).pack(side="left", padx=(0, 10))

        self.filtro_estado = ctk.CTkComboBox(
            filtros_frame,
            values=["Todos", "Abierto", "En Proceso", "Cerrado", "Cancelado"],
            width=120,
            height=35,
            command=self._filtrar_tickets
        )
        self.filtro_estado.set("Todos")
        self.filtro_estado.pack(side="left", padx=(0, 15))

        # Filtro por prioridad
        ctk.CTkLabel(
            filtros_frame,
            text="Prioridad:",
            text_color=self.colores["texto_oscuro"],
            font=("Lato Light", 12)
        ).pack(side="left", padx=(0, 10))

        self.filtro_prioridad = ctk.CTkComboBox(
            filtros_frame,
            values=["Todas", "Urgente", "Normal", "Baja"],
            width=120,
            height=35,
            command=self._filtrar_tickets
        )
        self.filtro_prioridad.set("Todas")
        self.filtro_prioridad.pack(side="left")

        # Búsqueda
        self.buscar_ticket_entry = ctk.CTkEntry(
            filtros_frame,
            placeholder_text="🔍 Buscar...",
            width=150,
            height=35
        )
        self.buscar_ticket_entry.pack(side="right")
        self.buscar_ticket_entry.bind("<KeyRelease>", self._filtrar_tickets)

        # Lista de tickets
        self.tickets_scroll = ctk.CTkScrollableFrame(
            tickets_frame, 
            fg_color=self.colores["fondo"],
            corner_radius=8
        )
        self.tickets_scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Botón de asignación
        self.asignar_btn = ctk.CTkButton(
            tickets_frame,
            text="🎯 Asignar Ticket Seleccionado",
            font=("Lato Light", 14),
            height=40,
            fg_color=self.colores["primario"],
            hover_color="#D26900",
            command=self._asignar_ticket,
            state="disabled"
        )
        self.asignar_btn.pack(fill="x", padx=20, pady=(0, 20))

    def _cargar_datos(self):
        """Carga todos los datos iniciales."""
        self._cargar_tecnicos()
        self._cargar_tickets()

    def _cargar_tecnicos(self):
        """Carga y muestra los técnicos."""
        # Limpiar técnicos existentes
        for widget in self.tecnicos_scroll.winfo_children():
            widget.destroy()

        try:
            # Obtener todos los empleados
            empleados = self.gestor_campos.read("empleado", where={})
            
            if not empleados:
                self._mostrar_estado_vacio(self.tecnicos_scroll, "tecnicos")
                return

            for empleado in empleados:
                self._crear_card_tecnico(empleado)
            
        except Exception as e:
            CTkMessagebox(
                title="Error",
                message=f"Error al cargar empleados: {str(e)}",
                icon="cancel"
            )

    def _crear_card_tecnico(self, tecnico):
        """Crea una card para un técnico."""
        # Contar tickets asignados
        tickets_asignados = self._contar_tickets_tecnico(tecnico[0])
        color_estado = self.colores["exito"] if tickets_asignados < 3 else self.colores["advertencia"] if tickets_asignados < 6 else self.colores["peligro"]

        card_frame = ctk.CTkFrame(
            self.tecnicos_scroll,
            fg_color=self.colores["card"],
            corner_radius=8,
            border_width=2,
            border_color=color_estado
        )
        card_frame.pack(fill="x", pady=5, padx=5)

        # Header con nombre y especialidad
        header_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            header_frame,
            text=tecnico[2],
            text_color=self.colores["texto_oscuro"],
            font=("Lato Light", 14, "bold")
        ).pack(side="left")

        ctk.CTkLabel(
            header_frame,
            text=f"Tickets: {tickets_asignados}",
            text_color=color_estado,
            font=("Lato Light", 12, "bold")
        ).pack(side="right")

        # Información del técnico
        info_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        info_frame.pack(fill="x", padx=10, pady=(0, 10))

        ctk.CTkLabel(
            info_frame,
            text=f"📧 {tecnico[3]}",
            text_color=self.colores["texto_claro"],
            font=("Lato Light", 11),
            anchor="w"
        ).pack(fill="x")

        ctk.CTkLabel(
            info_frame,
            text=f"📞 {tecnico[4]}",
            text_color=self.colores["texto_claro"],
            font=("Lato Light", 11),
            anchor="w"
        ).pack(fill="x")

        ctk.CTkLabel(
            info_frame,
            text=f"📍 Zona: {tecnico[6]}",
            text_color=self.colores["texto_claro"],
            font=("Lato Light", 11),
            anchor="w"
        ).pack(fill="x")

        # Guardar referencia para selección
        card_frame.id_empleado = tecnico[0]
        card_frame.nombre = tecnico[2]
        card_frame.tickets_asignados = tickets_asignados
        card_frame.id_rol_base = tecnico[7]  # Guardar el rol para filtrado

        # Evento de clic para selección
        def seleccionar_tecnico(event):
            self._seleccionar_tecnico(card_frame)
        
        card_frame.bind("<Button-1>", seleccionar_tecnico)
        
        # Propagar el evento a todos los hijos
        for child in card_frame.winfo_children():
            child.bind("<Button-1>", seleccionar_tecnico)
            for subchild in child.winfo_children():
                subchild.bind("<Button-1>", seleccionar_tecnico)

    def _contar_tickets_tecnico(self, id_tecnico):
        """Cuenta los tickets asignados a un técnico."""
        try:
            tickets = self.gestor_campos.read(
                "tickets_soporte", 
                where={"id_empleado_asignado": id_tecnico}
            )
            return len(tickets) if tickets else 0
        except:
            return 0

    def _cargar_tickets(self):
        """Carga y muestra los tickets."""
        # Limpiar tickets existentes
        for widget in self.tickets_scroll.winfo_children():
            widget.destroy()

        try:
            # Obtener todos los tickets
            tickets = self.gestor_campos.read("tickets_soporte", where={})
            
            if not tickets:
                self._mostrar_estado_vacio(self.tickets_scroll, "tickets")
                return

            for ticket in tickets:
                self._crear_card_ticket(ticket)
            
        except Exception as e:
            CTkMessagebox(
                title="Error",
                message=f"Error al cargar tickets: {str(e)}",
                icon="cancel"
            )

    def _crear_card_ticket(self, ticket):
        """Crea una card para un ticket."""
        # Mapeo de prioridades a colores
        colores_prioridad = {
            "urgente": self.colores["peligro"],
            "normal": self.colores["advertencia"],
            "baja": self.colores["exito"]
        }
        
        # Mapeo de estados a iconos
        iconos_estado = {
            "abierto": "🟢",
            "en_proceso": "🟡",
            "cerrado": "🔵",
            "cancelado": "🔴"
        }

        card_frame = ctk.CTkFrame(
            self.tickets_scroll,
            fg_color=self.colores["card"],
            corner_radius=8,
            border_width=2,
            border_color=colores_prioridad.get(ticket[6], self.colores["primario"])
        )
        card_frame.pack(fill="x", pady=5, padx=5)

        # Header con ID y título
        header_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            header_frame,
            text=f"#{ticket[0]} - {ticket[3]}",
            text_color=self.colores["texto_oscuro"],
            font=("Lato Light", 14, "bold")
        ).pack(side="left")

        # Estado y prioridad
        estado_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        estado_frame.pack(side="right")

        ctk.CTkLabel(
            estado_frame,
            text=f"{iconos_estado.get(ticket[7], '⚪')} {ticket[7].replace('_', ' ').title()}",
            text_color=self.colores["texto_claro"],
            font=("Lato Light", 11)
        ).pack(side="right")

        ctk.CTkLabel(
            estado_frame,
            text=f"• {ticket[6].title()}",
            text_color=colores_prioridad.get(ticket[6], self.colores["texto_claro"]),
            font=("Lato Light", 11, "bold")
        ).pack(side="right", padx=(0, 10))

        # Descripción
        descripcion = ticket[4] or "Sin descripción"
        if len(descripcion) > 100:
            descripcion = descripcion[:100] + "..."
        
        ctk.CTkLabel(
            card_frame,
            text=descripcion,
            text_color=self.colores["texto_claro"],
            font=("Lato Light", 12),
            wraplength=500,
            justify="left"
        ).pack(fill="x", padx=10, pady=(0, 10))

        # Información adicional
        info_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        info_frame.pack(fill="x", padx=10, pady=(0, 10))

        # Fecha
        fecha_creacion = ticket[8] or "Fecha desconocida"
        ctk.CTkLabel(
            info_frame,
            text=f"📅 {fecha_creacion}",
            text_color=self.colores["texto_claro"],
            font=("Lato Light", 10)
        ).pack(side="left")

        # Técnico asignado (si tiene)
        if ticket[2]:  # id_empleado_asignado
            tecnico = self._obtener_tecnico_por_id(ticket[2])
            if tecnico:
                ctk.CTkLabel(
                    info_frame,
                    text=f"👨‍💻 {tecnico[2]}",
                    text_color=self.colores["info"],
                    font=("Lato Light", 10)
                ).pack(side="right")

        # Botones de acción
        acciones_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        acciones_frame.pack(fill="x", padx=10, pady=(0, 10))

        if ticket[7] == "abierto":
            ctk.CTkButton(
                acciones_frame,
                text="Asignar",
                width=80,
                height=25,
                fg_color=self.colores["primario"],
                hover_color="#D26900",
                font=("Lato Light", 10),
                command=lambda t=ticket: self._preparar_asignacion(t)
            ).pack(side="left", padx=(0, 5))

        # Botón Editar - SIEMPRE visible
        btn_editar = ctk.CTkButton(
            acciones_frame,
            text="Editar",
            width=80,
            height=25,
            fg_color=self.colores["info"],
            hover_color="#2980B9",
            font=("Lato Light", 10),
            command=lambda t=ticket: self._editar_ticket(t)
        )
        btn_editar.pack(side="left", padx=5)

        # Botón Eliminar - SIEMPRE visible
        btn_eliminar = ctk.CTkButton(
            acciones_frame,
            text="Eliminar",
            width=80,
            height=25,
            fg_color=self.colores["peligro"],
            hover_color="#C0392B",
            font=("Lato Light", 10),
            command=lambda t=ticket: self._eliminar_ticket(t)
        )
        btn_eliminar.pack(side="left", padx=5)

        # Guardar referencia para selección
        card_frame.id_ticket = ticket[0]
        card_frame.ticket_data = ticket

        # Evento de clic para selección (solo en áreas que no son botones)
        def seleccionar_ticket(event):
            # Verificar que no se hizo clic en un botón
            widget_clicked = event.widget
            if not isinstance(widget_clicked, ctk.CTkButton):
                self._seleccionar_ticket(card_frame)
        
        card_frame.bind("<Button-1>", seleccionar_ticket)
        
        # Propagar el evento solo a los elementos que NO son botones
        for child in card_frame.winfo_children():
            if not isinstance(child, ctk.CTkButton) and child != acciones_frame:
                child.bind("<Button-1>", seleccionar_ticket)
                for subchild in child.winfo_children():
                    if not isinstance(subchild, ctk.CTkButton):
                        subchild.bind("<Button-1>", seleccionar_ticket)

    def _obtener_tecnico_por_id(self, id_tecnico):
        """Obtiene los datos de un técnico por su ID."""
        try:
            tecnicos = self.gestor_campos.read("empleado", where={"id_empleado": id_tecnico})
            return tecnicos[0] if tecnicos else None
        except:
            return None

    def _seleccionar_tecnico(self, tecnico_frame):
        """Selecciona un técnico."""
        # Quitar selección anterior
        for widget in self.tecnicos_scroll.winfo_children():
            if hasattr(widget, 'id_empleado'):
                # Restaurar color original basado en tickets asignados
                tickets = widget.tickets_asignados
                color_original = self.colores["exito"] if tickets < 3 else self.colores["advertencia"] if tickets < 6 else self.colores["peligro"]
                widget.configure(border_color=color_original)
        
        # Seleccionar nuevo
        tecnico_frame.configure(border_color=self.colores["info"])
        self.tecnico_seleccionado = tecnico_frame
        
        # Actualizar botón de asignación
        self._actualizar_boton_asignar()

    def _seleccionar_ticket(self, ticket_frame):
        """Selecciona un ticket."""
        # Quitar selección anterior
        for widget in self.tickets_scroll.winfo_children():
            if hasattr(widget, 'id_ticket'):
                # Restaurar color original basado en prioridad
                ticket_data = widget.ticket_data
                colores_prioridad = {
                    "urgente": self.colores["peligro"],
                    "normal": self.colores["advertencia"],
                    "baja": self.colores["exito"]
                }
                color_original = colores_prioridad.get(ticket_data[6], self.colores["primario"])
                widget.configure(border_color=color_original)
        
        # Seleccionar nuevo
        ticket_frame.configure(border_color=self.colores["info"])
        self.ticket_seleccionado = ticket_frame
        
        # Actualizar botón de asignación
        self._actualizar_boton_asignar()

    def _actualizar_boton_asignar(self):
        """Actualiza el estado del botón de asignar."""
        if self.ticket_seleccionado and self.tecnico_seleccionado:
            self.asignar_btn.configure(state="normal")
        else:
            self.asignar_btn.configure(state="disabled")

    def _asignar_ticket(self):
        """Asigna el ticket seleccionado al técnico seleccionado."""
        if not self.ticket_seleccionado or not self.tecnico_seleccionado:
            return

        try:
            ticket_data = self.ticket_seleccionado.ticket_data
            
            # Preparar datos para actualización
            update_data = {
                "id_ticket": ticket_data[0],
                "id_cliente": ticket_data[1],
                "id_empleado_asignado": self.tecnico_seleccionado.id_empleado,
                "titulo": ticket_data[3],
                "descripcion": ticket_data[4],
                "tipo_problema": ticket_data[5],
                "prioridad": ticket_data[6],
                "estado": "en_proceso",  # Cambiar estado a "en proceso"
                "fecha_creacion": ticket_data[8],
                "fecha_cierre": ticket_data[9] if len(ticket_data) > 9 else None,
                "solucion": ticket_data[10] if len(ticket_data) > 10 else None
            }
            
            # Actualizar en base de datos
            success = self.gestor_campos.update("tickets_soporte", update_data)
            
            if success:
                CTkMessagebox(
                    title="Éxito",
                    message=f"Ticket #{ticket_data[0]} asignado a {self.tecnico_seleccionado.nombre}",
                    icon="check"
                )
                
                # Recargar datos
                self._actualizar_todo()
                
            else:
                CTkMessagebox(
                    title="Error",
                    message="Error al asignar el ticket",
                    icon="cancel"
                )
            
        except Exception as e:
            CTkMessagebox(
                title="Error",
                message=f"Error al asignar: {str(e)}",
                icon="cancel"
            )

    def _preparar_asignacion(self, ticket):
        """Prepara la asignación seleccionando automáticamente el ticket."""
        # Buscar el frame del ticket y seleccionarlo
        for widget in self.tickets_scroll.winfo_children():
            if hasattr(widget, 'id_ticket') and widget.id_ticket == ticket[0]:
                self._seleccionar_ticket(widget)
                break

    def _editar_ticket(self, ticket):
        """Abre la ventana para editar un ticket."""
        try:
            from gui.soporte.editar_ticket_window import EditarTicketWindow
            ventana = EditarTicketWindow(self, ticket)
            ventana.grab_set()  # Hacer la ventana modal
            self.wait_window(ventana)  # Esperar a que se cierre
            self._actualizar_todo()  # Actualizar después de cerrar
        except Exception as e:
            CTkMessagebox(
                title="Error",
                message=f"No se pudo abrir el editor: {str(e)}",
                icon="cancel"
            )

    def _eliminar_ticket(self, ticket):
        """Elimina un ticket después de confirmación."""
        confirmar = CTkMessagebox(
            title="Confirmar eliminación",
            message=f"¿Estás seguro de eliminar el ticket #{ticket[0]}?",
            option_1="Cancelar",
            option_2="Eliminar",
            icon="warning"
        )
        
        if confirmar.get() == "Eliminar":
            try:
                if self.gestor_campos.delete("tickets_soporte", {"id_ticket": ticket[0]}):
                    CTkMessagebox(
                        title="Éxito",
                        message="Ticket eliminado correctamente",
                        icon="check"
                    )
                    self._actualizar_todo()
                else:
                    CTkMessagebox(
                        title="Error",
                        message="Error al eliminar el ticket",
                        icon="cancel"
                    )
            except Exception as e:
                CTkMessagebox(
                    title="Error",
                    message=f"Error al eliminar: {str(e)}",
                    icon="cancel"
                )

    def _filtrar_empleados_por_tipo(self, event=None):
        """Filtra empleados por tipo (rol)."""
        tipo_seleccionado = self.filtro_tipo_empleado.get()
        
        # Mapeo de tipos a id_rol_base
        mapeo_roles = {
            "Todos": None,
            "Técnico": 1,
            "Administrador": 2,
            "Secretaria": 3
        }
        
        id_rol = mapeo_roles.get(tipo_seleccionado)
        
        for widget in self.tecnicos_scroll.winfo_children():
            if hasattr(widget, 'id_rol_base'):
                if id_rol is None or widget.id_rol_base == id_rol:
                    widget.pack(fill="x", pady=5, padx=5)
                else:
                    widget.pack_forget()

    def _filtrar_tecnicos(self, event=None):
        """Filtra la lista de técnicos por nombre."""
        texto = self.buscar_tecnico_entry.get().lower()
        
        for widget in self.tecnicos_scroll.winfo_children():
            if hasattr(widget, 'nombre'):
                nombre = widget.nombre.lower()
                if texto in nombre:
                    widget.pack(fill="x", pady=5, padx=5)
                else:
                    widget.pack_forget()

    def _filtrar_tickets(self, event=None):
        """Filtra la lista de tickets."""
        texto = self.buscar_ticket_entry.get().lower()
        estado = self.filtro_estado.get().lower()
        prioridad = self.filtro_prioridad.get().lower()

        for widget in self.tickets_scroll.winfo_children():
            if hasattr(widget, 'ticket_data'):
                ticket = widget.ticket_data
                titulo = ticket[3].lower()
                descripcion = (ticket[4] or "").lower()
                ticket_estado = ticket[7].lower().replace('_', ' ')
                ticket_prioridad = ticket[6].lower()
                
                # Aplicar filtros
                muestra = True
                
                if texto and texto not in titulo and texto not in descripcion:
                    muestra = False
                
                if estado != "todos" and estado not in ticket_estado:
                    muestra = False
                
                if prioridad != "todas" and prioridad not in ticket_prioridad:
                    muestra = False
                
                if muestra:
                    widget.pack(fill="x", pady=5, padx=5)
                else:
                    widget.pack_forget()

    def _mostrar_estado_vacio(self, parent, tipo):
        """Muestra un estado vacío."""
        mensajes = {
            "tickets": "No hay tickets disponibles",
            "tecnicos": "No hay empleados disponibles"
        }
        
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(expand=True, fill="both")
        
        ctk.CTkLabel(
            frame,
            text="📭",
            text_color=self.colores["texto_claro"],
            font=("Lato Light", 48)
        ).pack(pady=10)
        
        ctk.CTkLabel(
            frame,
            text=mensajes[tipo],
            text_color=self.colores["texto_claro"],
            font=("Lato Light", 16)
        ).pack()

    def _actualizar_todo(self):
        """Actualiza todos los datos."""
        self._cargar_tecnicos()
        self._cargar_tickets()
        
        # Resetear selecciones
        self.ticket_seleccionado = None
        self.tecnico_seleccionado = None
        self.asignar_btn.configure(state="disabled")

    def _abrir_nuevo_ticket(self):
        """Abre el formulario para crear nuevo ticket."""
        try:
            from gui.soporte.nuevo_ticket_window import NuevoTicketWindow
            ventana = NuevoTicketWindow(self)
            ventana.grab_set()  # Hacer la ventana modal
            self.wait_window(ventana)  # Esperar a que se cierre
            self._actualizar_todo()  # Actualizar después de cerrar
        except Exception as e:
            CTkMessagebox(
                title="Error",
                message=f"No se pudo abrir el formulario: {str(e)}",
                icon="cancel"
            )
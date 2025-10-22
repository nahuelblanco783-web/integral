import customtkinter as ctk
from db.gestor_campos import GestorCampos
from CTkMessagebox import CTkMessagebox
import datetime

class EditarTicketWindow(ctk.CTkToplevel):
    """Ventana para editar tickets existentes"""

    def __init__(self, parent, ticket, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.parent = parent
        self.ticket = ticket
        self.gestor_campos = GestorCampos()
        
        # Guardar el estado original del ticket
        self.estado_original = ticket[7]
        self.empleado_asignado_original = ticket[2]
        
        self.title(f"Editar Ticket #{ticket[0]}")
        self.geometry("500x600")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        self._crear_interfaz()
        self._cargar_datos()
        self._centrar_ventana()

    def _crear_interfaz(self):
        """Crea la interfaz del formulario con scrollbar."""
        # Título
        ctk.CTkLabel(
            self,
            text=f"Editar Ticket #{self.ticket[0]}",
            font=("Lato Light", 20, "bold")
        ).pack(pady=20)
        
        # Frame principal con scroll
        main_frame = ctk.CTkScrollableFrame(self, height=450)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Formulario
        form_frame = ctk.CTkFrame(main_frame)
        form_frame.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Campos del formulario
        campos = [
            ("Título del Ticket", "entry"),
            ("Descripción del Problema", "textbox"),
            ("Tipo de Problema", "combo_tipo"),
            ("Prioridad", "combo_prioridad"),
            ("Estado", "combo_estado")
        ]
        
        self.widgets = {}
        
        for i, (campo, tipo) in enumerate(campos):
            # Label
            ctk.CTkLabel(
                form_frame,
                text=campo + ":",
                font=("Lato Light", 14),
                anchor="w"
            ).grid(row=i*2, column=0, padx=20, pady=(15, 5), sticky="w")
            
            if tipo == "entry":
                widget = ctk.CTkEntry(
                    form_frame, 
                    width=400,
                    height=35
                )
                widget.grid(row=i*2+1, column=0, padx=20, pady=(0, 15), sticky="w")
            
            elif tipo == "textbox":
                widget = ctk.CTkTextbox(
                    form_frame, 
                    width=400, 
                    height=100,
                    border_width=1
                )
                widget.grid(row=i*2+1, column=0, padx=20, pady=(0, 15), sticky="w")
            
            elif tipo == "combo_tipo":
                display_values = ["Problema de Conexión", "Problema de Facturación", "Configuración", "Problema Técnico", "Otros"]
                widget = ctk.CTkComboBox(
                    form_frame, 
                    values=display_values, 
                    width=400,
                    height=35
                )
                widget.grid(row=i*2+1, column=0, padx=20, pady=(0, 15), sticky="w")
            
            elif tipo == "combo_prioridad":
                display_values = ["Urgente", "Normal", "Baja"]
                widget = ctk.CTkComboBox(
                    form_frame, 
                    values=display_values, 
                    width=400,
                    height=35
                )
                widget.grid(row=i*2+1, column=0, padx=20, pady=(0, 15), sticky="w")
            
            elif tipo == "combo_estado":
                display_values = ["Abierto", "En Proceso", "Cerrado", "Cancelado"]
                widget = ctk.CTkComboBox(
                    form_frame, 
                    values=display_values, 
                    width=400,
                    height=35
                )
                widget.grid(row=i*2+1, column=0, padx=20, pady=(0, 15), sticky="w")
            
            self.widgets[campo] = widget
        
        # Información de cliente (solo lectura)
        ctk.CTkLabel(
            form_frame,
            text="Cliente:",
            font=("Lato Light", 14),
            anchor="w"
        ).grid(row=10, column=0, padx=20, pady=(15, 5), sticky="w")
        
        self.cliente_label = ctk.CTkLabel(
            form_frame,
            text="Cargando...",
            font=("Lato Light", 12),
            text_color="gray",
            anchor="w"
        )
        self.cliente_label.grid(row=11, column=0, padx=20, pady=(0, 15), sticky="w")
        
        # Información de empleado asignado (solo lectura)
        ctk.CTkLabel(
            form_frame,
            text="Empleado Asignado:",
            font=("Lato Light", 14),
            anchor="w"
        ).grid(row=12, column=0, padx=20, pady=(15, 5), sticky="w")
        
        self.empleado_label = ctk.CTkLabel(
            form_frame,
            text="Sin asignar",
            font=("Lato Light", 12),
            text_color="gray",
            anchor="w"
        )
        self.empleado_label.grid(row=13, column=0, padx=20, pady=(0, 15), sticky="w")
        
        # Botones (fuera del scroll)
        btn_frame = ctk.CTkFrame(self, fg_color="transparent", height=60)
        btn_frame.pack(fill="x", padx=20, pady=10)
        btn_frame.pack_propagate(False)
        
        ctk.CTkButton(
            btn_frame,
            text="Cancelar",
            width=120,
            height=40,
            fg_color="#95A5A6",
            hover_color="#7F8C8D",
            command=self.destroy
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(
            btn_frame,
            text="Guardar Cambios",
            width=120,
            height=40,
            fg_color="#E57819",
            hover_color="#D26900",
            command=self._guardar_cambios
        ).pack(side="left", padx=(10, 0))

    def _cargar_datos(self):
        """Carga los datos del ticket en el formulario."""
        try:
            # Cargar datos del ticket
            self.widgets["Título del Ticket"].insert(0, self.ticket[3])
            self.widgets["Descripción del Problema"].insert("1.0", self.ticket[4] or "")
            
            # Configurar combos
            tipo_problema_map = {
                "conexion": "Problema de Conexión",
                "facturacion": "Problema de Facturación", 
                "configuracion": "Configuración",
                "tecnico": "Problema Técnico",
                "otros": "Otros"
            }
            prioridad_map = {
                "urgente": "Urgente",
                "normal": "Normal", 
                "baja": "Baja"
            }
            estado_map = {
                "abierto": "Abierto",
                "en_proceso": "En Proceso",
                "cerrado": "Cerrado", 
                "cancelado": "Cancelado"
            }
            
            self.widgets["Tipo de Problema"].set(tipo_problema_map.get(self.ticket[5], "Problema de Conexión"))
            self.widgets["Prioridad"].set(prioridad_map.get(self.ticket[6], "Normal"))
            self.widgets["Estado"].set(estado_map.get(self.ticket[7], "Abierto"))
            
            # Cargar información del cliente
            cliente_data = self.gestor_campos.read("cliente", where={"id_cliente": self.ticket[1]})
            if cliente_data:
                cliente = cliente_data[0]
                self.cliente_label.configure(
                    text=f"{cliente[2]} (DNI: {cliente[1]}) - 📞 {cliente[4]}"
                )
            else:
                self.cliente_label.configure(text="Cliente no encontrado")
            
            # Cargar información del empleado asignado
            if self.ticket[2]:  # id_empleado_asignado
                empleado_data = self.gestor_campos.read("empleado", where={"id_empleado": self.ticket[2]})
                if empleado_data:
                    empleado = empleado_data[0]
                    self.empleado_label.configure(
                        text=f"{empleado[2]} - 📧 {empleado[3]}",
                        text_color="#3498DB"
                    )
                else:
                    self.empleado_label.configure(text="Empleado no encontrado", text_color="red")
            else:
                self.empleado_label.configure(text="Sin asignar", text_color="gray")
            
        except Exception as e:
            CTkMessagebox(
                title="Error",
                message=f"Error al cargar datos: {str(e)}",
                icon="cancel"
            )

    def _centrar_ventana(self):
        """Centra la ventana en la pantalla."""
        self.update_idletasks()
        ancho = 500
        alto = 600
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def _guardar_cambios(self):
        """Guarda los cambios del ticket."""
        try:
            # Obtener valores
            titulo = self.widgets["Título del Ticket"].get().strip()
            descripcion = self.widgets["Descripción del Problema"].get("1.0", "end-1c").strip()
            
            # Obtener valores reales de los combos
            tipo_problema_display = self.widgets["Tipo de Problema"].get()
            prioridad_display = self.widgets["Prioridad"].get()
            estado_display = self.widgets["Estado"].get()
            
            # Mapear display values a valores reales
            tipo_problema_map = {
                "Problema de Conexión": "conexion",
                "Problema de Facturación": "facturacion",
                "Configuración": "configuracion",
                "Problema Técnico": "tecnico",
                "Otros": "otros"
            }
            prioridad_map = {
                "Urgente": "urgente",
                "Normal": "normal",
                "Baja": "baja"
            }
            estado_map = {
                "Abierto": "abierto",
                "En Proceso": "en_proceso", 
                "Cerrado": "cerrado",
                "Cancelado": "cancelado"
            }
            
            tipo_problema = tipo_problema_map.get(tipo_problema_display, "conexion")
            prioridad = prioridad_map.get(prioridad_display, "normal")
            estado_nuevo = estado_map.get(estado_display, "abierto")
            
            # Validaciones
            if not titulo:
                CTkMessagebox(title="Error", message="El título es obligatorio", icon="cancel")
                return
            
            # Preparar datos para actualización
            update_data = {
                "id_ticket": self.ticket[0],
                "id_cliente": self.ticket[1],
                "titulo": titulo,
                "descripcion": descripcion,
                "tipo_problema": tipo_problema,
                "prioridad": prioridad,
                "estado": estado_nuevo,
                "fecha_creacion": self.ticket[8],
                "fecha_cierre": self.ticket[9] if len(self.ticket) > 9 else None,
                "solucion": self.ticket[10] if len(self.ticket) > 10 else None
            }
            
            # LÓGICA MEJORADA: Gestión de empleado asignado según el estado
            
            # Si el ticket cambia a "cerrado" o "cancelado"
            if estado_nuevo in ["cerrado", "cancelado"]:
                # Desasignar empleado
                update_data["id_empleado_asignado"] = None
                
                # Agregar fecha de cierre si no existe
                if not update_data["fecha_cierre"]:
                    update_data["fecha_cierre"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Si el ticket cambia de "cerrado/cancelado" a "abierto"
            elif estado_nuevo == "abierto":
                update_data["id_empleado_asignado"] = None  # Sin asignar
                update_data["fecha_cierre"] = None  # Limpiar fecha de cierre
            
            # Si el ticket está en "en_proceso", mantener el empleado asignado
            elif estado_nuevo == "en_proceso":
                update_data["id_empleado_asignado"] = self.empleado_asignado_original
            
            # Actualizar en la base de datos
            success = self.gestor_campos.update("tickets_soporte", update_data)
            
            if success:
                # Mensaje personalizado según el cambio de estado
                mensaje = "Ticket actualizado correctamente"
                
                if estado_nuevo in ["cerrado", "cancelado"] and self.estado_original not in ["cerrado", "cancelado"]:
                    if self.empleado_asignado_original:
                        empleado_data = self.gestor_campos.read("empleado", where={"id_empleado": self.empleado_asignado_original})
                        if empleado_data:
                            nombre_empleado = empleado_data[0][2]
                            mensaje = f"Ticket {estado_display.lower()} correctamente.\nEmpleado {nombre_empleado} desasignado y liberado."
                
                CTkMessagebox(
                    title="Éxito", 
                    message=mensaje, 
                    icon="check"
                )
                self.destroy()
                if hasattr(self.parent, '_actualizar_todo'):
                    self.parent._actualizar_todo()
            else:
                CTkMessagebox(
                    title="Error", 
                    message="Error al actualizar el ticket", 
                    icon="cancel"
                )
            
        except Exception as e:
            CTkMessagebox(
                title="Error", 
                message=f"Error inesperado: {str(e)}", 
                icon="cancel"
            )
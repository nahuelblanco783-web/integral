import customtkinter as ctk
from db.gestor_campos import GestorCampos
from CTkMessagebox import CTkMessagebox
import datetime

class NuevoTicketWindow(ctk.CTkToplevel):
    """Ventana para crear nuevos tickets - Versión con Scrollbar"""

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.parent = parent
        self.gestor_campos = GestorCampos()
        
        self.title("Nuevo Ticket de Soporte")
        self.geometry("500x550")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        
        self._crear_interfaz()
        self._centrar_ventana()

    def _crear_interfaz(self):
        """Crea la interfaz del formulario con scrollbar."""
        # Título
        ctk.CTkLabel(
            self,
            text="Crear Nuevo Ticket",
            font=("Lato Light", 20, "bold")
        ).pack(pady=20)
        
        # Frame principal con scroll
        main_frame = ctk.CTkScrollableFrame(self, height=400)
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
            ("Cliente (DNI)", "entry")
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
                    height=35,
                    placeholder_text=f"Ingrese {campo.lower()}..."
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
                widget.set(display_values[0])
                widget.grid(row=i*2+1, column=0, padx=20, pady=(0, 15), sticky="w")
                
            elif tipo == "combo_prioridad":
                display_values = ["Urgente", "Normal", "Baja"]
                widget = ctk.CTkComboBox(
                    form_frame, 
                    values=display_values, 
                    width=400,
                    height=35
                )
                widget.set(display_values[1])  # Normal por defecto
                widget.grid(row=i*2+1, column=0, padx=20, pady=(0, 15), sticky="w")
            
            self.widgets[campo] = widget
        
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
            text="Crear Ticket",
            width=120,
            height=40,
            fg_color="#E57819",
            hover_color="#D26900",
            command=self._crear_ticket
        ).pack(side="left", padx=(10, 0))

    def _centrar_ventana(self):
        """Centra la ventana en la pantalla."""
        self.update_idletasks()
        ancho = 500
        alto = 550
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def _crear_ticket(self):
        """Crea el nuevo ticket en la base de datos."""
        try:
            # Obtener valores
            titulo = self.widgets["Título del Ticket"].get().strip()
            descripcion = self.widgets["Descripción del Problema"].get("1.0", "end-1c").strip()
            dni_cliente = self.widgets["Cliente (DNI)"].get().strip()
            
            # Obtener valores reales de los combos
            tipo_problema_display = self.widgets["Tipo de Problema"].get()
            prioridad_display = self.widgets["Prioridad"].get()
            
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
            
            tipo_problema = tipo_problema_map.get(tipo_problema_display, "conexion")
            prioridad = prioridad_map.get(prioridad_display, "normal")
            
            # Validaciones básicas
            if not titulo or not descripcion or not dni_cliente:
                CTkMessagebox(
                    title="Error", 
                    message="Todos los campos son obligatorios", 
                    icon="cancel"
                )
                return
            
            # Buscar cliente por DNI
            cliente_data = self.gestor_campos.read("cliente", where={"dni": dni_cliente})
            if not cliente_data:
                CTkMessagebox(
                    title="Error", 
                    message="Cliente no encontrado. Verifique el DNI.", 
                    icon="cancel"
                )
                return
            
            id_cliente = cliente_data[0][0]
            
            # Crear ticket usando diccionario (más robusto)
            ticket_data = {
                "id_cliente": id_cliente,
                "titulo": titulo,
                "descripcion": descripcion,
                "tipo_problema": tipo_problema,
                "prioridad": prioridad,
                "estado": "abierto",
                "fecha_creacion": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            success = self.gestor_campos.create("tickets_soporte", ticket_data)
            
            if success:
                CTkMessagebox(
                    title="Éxito", 
                    message="Ticket creado correctamente", 
                    icon="check"
                )
                self.destroy()
                if hasattr(self.parent, '_actualizar_todo'):
                    self.parent._actualizar_todo()
            else:
                CTkMessagebox(
                    title="Error", 
                    message="Error al crear el ticket en la base de datos", 
                    icon="cancel"
                )
                
        except Exception as e:
            CTkMessagebox(
                title="Error", 
                message=f"Error inesperado: {str(e)}", 
                icon="cancel"
            )
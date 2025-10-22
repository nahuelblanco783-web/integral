# nuevo_equipo_window.py
import customtkinter as ctk
import time
from db.gestor_campos import GestorCampos
from CTkMessagebox import CTkMessagebox

class NuevoEquipo(ctk.CTkToplevel):
    """Toplevel para crear un nuevo equipo"""

    def __init__(self, fg_color="white", **kwargs):
        super().__init__(fg_color=fg_color, **kwargs)

        self.attributes('-topmost', True)
        self.configure(width=800, height=600)
        self.resizable(0, 0)
        self.title('Ingresar nuevo equipo')

        # Instancia del gestor
        self.gestor_campos = GestorCampos()
        self.campos_equipo = self.gestor_campos.get_campos("equipos")[1:]  # Excluir ID

        # Estados posibles para el combo box
        self.estados_posibles = ['activo', 'inactivo', 'defectuoso', 'en_mantenimiento']
        
        # Tipos posibles para el combo box
        self.tipos_posibles = ['router', 'ont', 'antena', 'modem']
        

        
        # Cantidad de equipos a cargar
        self.cantidad_equipos = 1
        self._procesando = False
        

        self._crear_interfaz()

    def _crear_interfaz(self):
        """Crea la interfaz de forma dinámica basada en los campos de la tabla"""
        self.entries = {}
        # En la sección donde se crea el botón decrementar, agregar:
        
        for i, campo in enumerate(self.campos_equipo):
            row = i // 2
            col = i % 2

            # Label
            ctk.CTkLabel(
                master=self,
                text=f"{campo}:",
                font=("Lato Light", 16),
                text_color="black"
            ).grid(row=row*2, column=col, padx=(50, 25), pady=(25, 0) if row == 0 else (15, 0), sticky="w")

            # Si es el campo de estado, usar combobox
            if campo.lower() == 'estado':
                combobox = ctk.CTkComboBox(
                    master=self,
                    values=self.estados_posibles,
                    width=150,
                    height=40,
                    corner_radius=0,
                    fg_color='#D9D9D9',
                    border_width=0,
                    text_color='black',
                    dropdown_fg_color='white',
                    dropdown_text_color='black'
                )
                combobox.set(self.estados_posibles[0])
                combobox.grid(row=row*2+1, column=col, padx=(50, 25) if col == 0 else (25, 50),
                pady=(5, 25) if i == len(self.campos_equipo)-1 else (5, 0))
                self.entries[campo] = combobox
            # Si es el campo de tipo equipo, usar combobox con tipos de equipos
            elif campo.lower() == 'tipo equipo' or 'tipo' in campo.lower():
                combobox = ctk.CTkComboBox(
                    master=self,
                    values=self.tipos_posibles,
                    width=150,
                    height=40,
                    corner_radius=0,
                    fg_color='#D9D9D9',
                    border_width=0,
                    text_color='black',
                    dropdown_fg_color='white',
                    dropdown_text_color='black'
                )
                combobox.set(self.tipos_posibles[0])
                combobox.grid(row=row*2+1, column=col, padx=(50, 25) if col == 0 else (25, 50),
                pady=(5, 25) if i == len(self.campos_equipo)-1 else (5, 0))
                self.entries[campo] = combobox
            else:
                # Entry normal para otros campos
                entry = ctk.CTkEntry(
                    master=self,
                    width=150,
                    height=40,
                    corner_radius=0,
                    fg_color='#D9D9D9',
                    placeholder_text=f'Ingrese {campo.lower()}...',
                    border_width=0,
                    text_color='black',
                    placeholder_text_color='black'
                )
                entry.grid(row=row*2+1, column=col, padx=(50, 25) if col == 0 else (25, 50),
                pady=(5, 25) if i == len(self.campos_equipo)-1 else (5, 0))
                self.entries[campo] = entry

        # Cantidad de equipos
        total_rows = ((len(self.campos_equipo) - 1) // 2) * 2 + 2
        
        ctk.CTkLabel(
            master=self,
            text="Cantidad:",
            font=("Lato Light", 16),
            text_color="black"
        ).grid(row=total_rows, column=0, padx=(50, 25), pady=(15, 0), sticky="w")
        
        # Frame para cantidad y botón
        cantidad_frame = ctk.CTkFrame(master=self, fg_color="white")
        cantidad_frame.grid(row=total_rows+1, column=0, padx=(50, 25), pady=(5, 0), sticky="w")
        
        self.decrementar_boton = ctk.CTkButton(
            master=cantidad_frame,
            text="-",
            corner_radius=0,
            border_width=0,
            width=40,
            height=40,
            fg_color='#E57819',
            hover_color='orange',
            command=self.decrementar_cantidad
        )
        self.decrementar_boton.pack(side="left")
        
        self.cantidad_label = ctk.CTkLabel(
            master=cantidad_frame,
            text="1",
            font=("Lato Light", 20),
            text_color="black",
            width=50
        )
        self.cantidad_label.pack(side="left", padx=10)
        
        self.incrementar_boton = ctk.CTkButton(
            master=cantidad_frame,
            text="+",
            corner_radius=0,
            border_width=0,
            width=40,
            height=40,
            fg_color='#E57819',
            hover_color='orange',
            command=self.incrementar_cantidad
        )
        self.incrementar_boton.pack(side="left")
        self.decrementar_boton.configure(state="disabled")  # Inicialmente deshabilitado

        
        self._actualizar_cantidad_label()
        
        # Barra de progreso para inserciones múltiples
        self.progressbar = ctk.CTkProgressBar(
            master=self,
            width=300,
            height=18,
            corner_radius=0,
            mode="determinate"
        )
        self.progressbar.grid(row=total_rows+2, column=0, columnspan=2, padx=(50, 50), pady=(15, 5), sticky="ew")
        self.progressbar.set(0)
        self.progressbar.grid_remove()
        
        self.progress_label = ctk.CTkLabel(
            master=self,
            text="",
            font=("Lato Light", 14),
            text_color="black"
        )
        self.progress_label.grid(row=total_rows+3, column=0, columnspan=2, padx=(50, 50), sticky="w")
        self.progress_label.grid_remove()
        
        # Botón Aceptar
        self.aceptar_boton = ctk.CTkButton(
            master=self,
            text='Aceptar',
            corner_radius=0,
            border_width=0,
            width=150,
            height=40,
            fg_color='#E57819',
            hover_color='orange',
            command=self.aceptar_equipo
        )
        # Colocar el botón en la posición adecuada
        self.aceptar_boton.grid(row=total_rows+4, column=1, padx=(25, 50), pady=(15, 25))

    def incrementar_cantidad(self):
        """Incrementa la cantidad de equipos a cargar"""
        self.cantidad_equipos += 1
        self._actualizar_cantidad_label()
        
        # Habilitar el botón de decremento si estaba deshabilitado
        if self.decrementar_boton.cget("state") == "disabled":
            self.decrementar_boton.configure(state="normal")
    
    def decrementar_cantidad(self):
        """Decrementa la cantidad de equipos a cargar (mínimo 1)"""
        if self.cantidad_equipos > 1:
            self.cantidad_equipos -= 1
            self._actualizar_cantidad_label()
            
            # Actualizar estado del botón de decremento
            if self.cantidad_equipos == 1:
                self.decrementar_boton.configure(state="disabled")
            else:
                self.decrementar_boton.configure(state="normal")

    def _actualizar_cantidad_label(self):
        """Actualiza el label que muestra la cantidad de equipos"""
        self.cantidad_label.configure(text=str(self.cantidad_equipos))
        
    def _obtener_indice_campo(self, nombre_campo):
        """Obtiene el índice de un campo en la lista de campos"""
        try:
            return self.campos_equipo.index(nombre_campo)
        except ValueError:
            return -1
    
    def aceptar_equipo(self):
        """Guarda los nuevos equipos en la base de datos"""
        if self._procesando:
            return
            
        try:
            # Obtener valores de los campos
            valores_base = []
            serie_base = None
            for campo in self.campos_equipo:
                entry = self.entries[campo]
                valor = entry.get().strip()

                # Si id_cliente está vacío, asignar "0"
                if campo.lower() == 'id_cliente' and valor == "":
                    valor = "0"
                # Si fecha_instalacion está vacío, asignar "no instalado"
                elif campo.lower() == 'fecha_instalacion' and valor == "":
                    valor = "no instalado"

                # Guardar el valor base de la serie para generar variaciones
                if campo.lower() == 'serie':
                    serie_base = valor

                valores_base.append(valor)

            # Validar que los campos obligatorios no estén vacíos (excluyendo id_cliente y fecha_instalacion)
            campos_validos = True
            campos_faltantes = []
            
            for campo, valor in zip(self.campos_equipo, valores_base):
                if campo.lower() not in ['id_cliente', 'fecha_instalacion']:
                    if valor == "":
                        campos_validos = False
                        campos_faltantes.append(campo)

            if not campos_validos:
                CTkMessagebox(
                    master=self,
                    title='Error',
                    message=f'Por favor complete los siguientes campos obligatorios: {", ".join(campos_faltantes)}',
                    icon='cancel'
                )
                return

            # Verificar que se ingresó una serie base
            if not serie_base:
                CTkMessagebox(
                    master=self,
                    title='Error',
                    message='El campo Serie es obligatorio',
                    icon='cancel'
                )
                return

            # Configurar progreso
            self._procesando = True
            self.progressbar.grid()
            self.progress_label.grid()
            self.progressbar.set(0)
            
            # Insertar en la base de datos la cantidad de veces especificada
            equipos_insertados = 0
            
            for i in range(self.cantidad_equipos):
                # Actualizar progreso
                progreso = (i + 1) / self.cantidad_equipos
                self.progressbar.set(progreso)
                self.progress_label.configure(text=f"Insertando equipo {i + 1} de {self.cantidad_equipos}")
                self.update()
                
                # Crear una copia de los valores base para modificar la serie
                valores_equipo = list(valores_base)
                
                # Generar serie única para cada equipo
                if self.cantidad_equipos > 1:
                    serie_unica = f"{serie_base}-{i+1:03d}"  # Ejemplo: "ABC123-001", "ABC123-002", etc.
                else:
                    serie_unica = serie_base  # Para un solo equipo, usar la serie original

                # Reemplazar la serie en los valores
                indice_serie = self._obtener_indice_campo('Serie')
                if indice_serie != -1:
                    valores_equipo[indice_serie] = serie_unica
                
                # Insertar equipo
                bandera_equipo = self.gestor_campos.create('equipos', valores_equipo)
                if bandera_equipo:
                    equipos_insertados += 1
                
                # Pequeña pausa para visualizar el progreso
                time.sleep(0.1)

            # Ocultar barra de progreso
            self.progressbar.grid_remove()
            self.progress_label.grid_remove()
            self._procesando = False

            if equipos_insertados == self.cantidad_equipos:
                CTkMessagebox(
                    master=self,
                    title='Información',
                    message=f'{equipos_insertados} equipo(s) ha(n) sido ingresado(s) exitosamente',
                    option_1='Aceptar',
                    icon='info'
                )
                self.destroy()
            else:
                CTkMessagebox(
                    master=self,
                    title='Error',
                    message=f'Solo se ingresaron {equipos_insertados} de {self.cantidad_equipos} equipos',
                    icon='cancel'
                )

        except Exception as e:
            self._procesando = False
            # Ocultar barra de progreso en caso de error
            self.progressbar.grid_remove()
            self.progress_label.grid_remove()
            CTkMessagebox(
                master=self,
                title='Error',
                message=f'Error: {str(e)}',
                icon='cancel'
            )
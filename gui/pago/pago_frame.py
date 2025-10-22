import customtkinter as ctk
import tkinter as tk
from PIL import Image
from CTkMessagebox import CTkMessagebox
from db.gestor_campos import GestorCampos
from datetime import datetime

class PagoFrame(ctk.CTkFrame):
    """Frame de gestif3n de pagos"""
    def __init__(self, master, user, **kwargs):
        super().__init__(master, **kwargs)
        self.user = user
        self.configure(corner_radius=0, border_width=0, fg_color='white')
        self.pack(fill='both', expand=True)

        # Crear submenfa siguiendo el mismo estilo que otros frames
        self._crear_submenu()
        # Espacio para el contenido principal del submenu Pago (usar grid en lugar de pack)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.content_frame = ctk.CTkFrame(self, fg_color='white')
        self.content_frame.grid(row=1, column=0, sticky='nsew', padx=25, pady=25)

    def _crear_submenu(self):
        """Crea el submenfa superior con logo y botones de accif3n."""
        self.columnconfigure(0, weight=1)

        self.sub_menu = ctk.CTkFrame(self, corner_radius=0, fg_color="#A4A4A4", height=80)
        self.sub_menu.grid(row=0, column=0, sticky="ew")

        # Logo pequef1o a la izquierda
        try:
            logo_img = ctk.CTkImage(
                light_image=Image.open("gui/images/integral.png"),
                dark_image=Image.open("gui/images/integral.png"),
                size=(35, 45),
            )
        except Exception:
            logo_img = None

        ctk.CTkLabel(
            self.sub_menu,
            text="  Integral Comunicaciones SRL",
            text_color="white",
            font=("Lato Light", 24),
            image=logo_img,
            compound="left",
        ).grid(row=0, column=0, padx=(25, 0), pady=5)

        # Espaciador para empujar los botones a la derecha
        self.sub_menu.columnconfigure(1, weight=1)

        botones_frame = ctk.CTkFrame(self.sub_menu, fg_color="transparent")
        botones_frame.grid(row=0, column=2, sticky="e", padx=25, pady=5)

        # Botones del submenu de Pago (placeholders para las acciones)
        btn_factura = ctk.CTkButton(
            botones_frame,
            text="Factura Electrónica",
            font=("Lato Light", 14),
            width=180,
            height=40,
            fg_color="#D9D9D9",
            hover_color="#BFBFBF",
            text_color="black",
            command=self.mostrar_form_factura
        )
        btn_factura.pack(side="left", padx=(0, 10))

        btn_cobros = ctk.CTkButton(
            botones_frame,
            text="Cobros Masivos",
            font=("Lato Light", 14),
            width=150,
            height=40,
            fg_color="#D9D9D9",
            hover_color="#BFBFBF",
            text_color="black",
            command=self.cobros_masivos
        )
        btn_cobros.pack(side="left", padx=(0, 10))

        btn_pasarelas = ctk.CTkButton(
            botones_frame,
            text="Pasarelas de Pago",
            font=("Lato Light", 14),
            width=170,
            height=40,
            fg_color="#D9D9D9",
            hover_color="#BFBFBF",
            text_color="black",
            command=self.gestion_pasarelas
        )
        btn_pasarelas.pack(side="left", padx=(0, 10))

        btn_auto = ctk.CTkButton(
            botones_frame,
            text="Auto Susp./Reconex.",
            font=("Lato Light", 14),
            width=170,
            height=40,
            fg_color="#D9D9D9",
            hover_color="#BFBFBF",
            text_color="black",
            command=self.automatizacion_suspension_reconexion
        )
        btn_auto.pack(side="left", padx=(0, 10))

        btn_reportes = ctk.CTkButton(
            botones_frame,
            text="Reportes y Estadísticas",
            font=("Lato Light", 14),
            width=220,
            height=40,
            fg_color="#D9D9D9",
            hover_color="#BFBFBF",
            text_color="black",
            command=self.reportes_estadisticas
        )
        btn_reportes.pack(side="left")

    # ------------------ Formulario embebido Factura Electrónica ------------------
    def mostrar_form_factura(self):
        """Renderiza el formulario de factura dentro de content_frame."""
        # Limpiar contenido previo
        for w in self.content_frame.winfo_children():
            w.destroy()

        # Instancia GestorCampos
        self.gestor = GestorCampos()

        form_frame = ctk.CTkFrame(self.content_frame, fg_color='white')
        form_frame.grid(row=0, column=0, sticky='nwe')

        # Selección de cliente (simple entry para buscar por DNI)
        ctk.CTkLabel(form_frame, text='DNI Cliente:', font=("Lato Light", 14)).grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.fact_dni_entry = ctk.CTkEntry(form_frame, width=200, height=32)
        self.fact_dni_entry.grid(row=0, column=1, padx=10, pady=10, sticky='w')

        buscar_btn = ctk.CTkButton(form_frame, text='Buscar', width=100, command=self._buscar_cliente_por_dni)
        buscar_btn.grid(row=0, column=2, padx=10, pady=10)

        self.fact_cliente_label = ctk.CTkLabel(form_frame, text='Cliente: N/D', font=("Lato Light", 12))
        self.fact_cliente_label.grid(row=1, column=0, columnspan=3, padx=10, pady=(0,10), sticky='w')

        # Fecha emision y vencimiento
        ctk.CTkLabel(form_frame, text='Fecha Emisión:', font=("Lato Light", 14)).grid(row=2, column=0, padx=10, pady=10, sticky='w')
        self.fact_fecha_emision = ctk.CTkEntry(form_frame, width=120)
        self.fact_fecha_emision.grid(row=2, column=1, sticky='w')
        self.fact_fecha_emision.insert(0, datetime.now().strftime('%Y-%m-%d'))

        ctk.CTkLabel(form_frame, text='Fecha Vto:', font=("Lato Light", 14)).grid(row=2, column=2, padx=10, pady=10, sticky='w')
        self.fact_fecha_vto = ctk.CTkEntry(form_frame, width=120)
        self.fact_fecha_vto.grid(row=2, column=3, sticky='w')
        # por defecto +30 dias
        self.fact_fecha_vto.insert(0, (datetime.now()).strftime('%Y-%m-%d'))

        # Items (simple tabla con descripcion y monto)
        items_frame = ctk.CTkFrame(self.content_frame, fg_color='white')
        items_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)

        ctk.CTkLabel(items_frame, text='Descripción', font=("Lato Light", 12)).grid(row=0, column=0, padx=5, sticky='w')
        ctk.CTkLabel(items_frame, text='Monto', font=("Lato Light", 12)).grid(row=0, column=1, padx=5, sticky='w')

        self.items_rows = []

        def _agregar_item():
            row = len(self.items_rows) + 1
            desc = ctk.CTkEntry(items_frame, width=400)
            desc.grid(row=row, column=0, padx=5, pady=3, sticky='w')
            monto = ctk.CTkEntry(items_frame, width=120)
            monto.grid(row=row, column=1, padx=5, pady=3, sticky='w')
            self.items_rows.append((desc, monto))

        agregar_btn = ctk.CTkButton(items_frame, text='+ Item', width=80, command=_agregar_item)
        agregar_btn.grid(row=0, column=2, padx=10)

        # Añadir una fila inicial
        _agregar_item()

        # Total y acciones
        acciones_frame = ctk.CTkFrame(self.content_frame, fg_color='white')
        acciones_frame.grid(row=2, column=0, sticky='e', padx=10, pady=10)

        self.total_label = ctk.CTkLabel(acciones_frame, text='Total: 0.00', font=("Lato Light", 14, 'bold'))
        self.total_label.grid(row=0, column=0, padx=10)

        calcular_btn = ctk.CTkButton(acciones_frame, text='Calcular Total', command=self._calcular_total)
        calcular_btn.grid(row=0, column=1, padx=10)

        guardar_btn = ctk.CTkButton(acciones_frame, text='Guardar Factura', fg_color='#E57819', command=self._guardar_factura)
        guardar_btn.grid(row=0, column=2, padx=10)

        cancelar_btn = ctk.CTkButton(acciones_frame, text='Cancelar', command=lambda: self.mostrar_placeholder())
        cancelar_btn.grid(row=0, column=3, padx=10)

    def _buscar_cliente_por_dni(self):
        dni = self.fact_dni_entry.get().strip()
        if not dni:
            CTkMessagebox(title='Error', message='Ingrese un DNI para buscar', icon='cancel')
            return
        resultados = self.gestor.read('cliente', where={'dni': dni})
        if resultados:
            cliente = resultados[0]
            self.fact_cliente = cliente
            self.fact_cliente_label.configure(text=f'Cliente: {cliente[2]} - {cliente[3]}')
        else:
            self.fact_cliente = None
            self.fact_cliente_label.configure(text='Cliente: N/D')
            CTkMessagebox(title='Info', message='No se encontró cliente con ese DNI', icon='info')

    def _calcular_total(self):
        total = 0.0
        for desc, monto in self.items_rows:
            try:
                val = float(monto.get() or 0)
            except ValueError:
                val = 0.0
            total += val
        self.total_label.configure(text=f'Total: {total:.2f}')

    def _guardar_factura(self):
        # Validaciones mínimas
        if not getattr(self, 'fact_cliente', None):
            CTkMessagebox(title='Error', message='No hay cliente seleccionado', icon='cancel')
            return

        fecha_em = self.fact_fecha_emision.get()
        fecha_vto = self.fact_fecha_vto.get()
        # Construir detalles
        detalles = []
        total = 0.0
        for desc, monto in self.items_rows:
            d = desc.get().strip()
            try:
                m = float(monto.get() or 0)
            except ValueError:
                m = 0.0
            if d or m:
                detalles.append(f"{d}:{m:.2f}")
                total += m

        detalles_str = ';'.join(detalles)

        valores = [
            self.fact_cliente[0],  # id_cliente
            fecha_em,
            fecha_vto,
            total,
            'pendiente',
            detalles_str
        ]

        created = self.gestor.create('facturas', values=valores)
        if created:
            CTkMessagebox(title='Éxito', message='Factura guardada correctamente', icon='check')
            self.mostrar_placeholder()
        else:
            CTkMessagebox(title='Error', message='No se pudo guardar la factura', icon='cancel')

    def mostrar_placeholder(self):
        # Vuelve al estado inicial del content_frame (vacío)
        for w in self.content_frame.winfo_children():
            w.destroy()
        ctk.CTkLabel(self.content_frame, text='Seleccione una acción del submenú', font=("Lato Light", 18)).grid(row=0, column=0, padx=20, pady=20)

    def cobros_masivos(self):
        """Interfaz y ejecución de cobros masivos: listar facturas pendientes, seleccionar y procesar pagos."""
        # Limpiar contenido previo
        for w in self.content_frame.winfo_children():
            w.destroy()

        self.gestor = GestorCampos()

        # Contenedor principal
        main = ctk.CTkFrame(self.content_frame, fg_color='white')
        main.grid(row=0, column=0, sticky='nsew')

        # Título
        ctk.CTkLabel(main, text='Cobros Masivos', font=("Lato Light", 18, 'bold')).grid(row=0, column=0, sticky='w', padx=10, pady=(10,5))

        # Frame scrollable para la lista de facturas
        scroll = ctk.CTkScrollableFrame(main, fg_color='white')
        scroll.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
        scroll.grid_columnconfigure(0, weight=1)

        # Obtener facturas pendientes
        try:
            facturas = self.gestor.read('facturas', where={'estado': 'pendiente'})
        except Exception as e:
            CTkMessagebox(title='Error', message=f'Error al leer facturas: {e}', icon='cancel')
            return

        if not facturas:
            ctk.CTkLabel(scroll, text='No hay facturas pendientes', font=("Lato Light", 14)).pack(padx=10, pady=10)
            return

        # Variables y mapeos
        self._cobros_check_vars = {}
        self._cobros_facturas_map = {}

        for f in facturas:
            # Asumimos esquema: (id_factura, id_cliente, fecha_emision, fecha_vencimiento, monto_total, estado, detalles)
            fid = f[0]
            id_cliente = f[1]
            fecha_em = f[2]
            monto = f[4]
            detalles = f[6] if len(f) > 6 else ''

            var = tk.BooleanVar(value=False)
            label = f"#{fid} — Cliente:{id_cliente} — {fecha_em} — Monto: {monto:.2f}"
            # Mostrar detalle como tooltip-text en el label del checkbox
            cb = ctk.CTkCheckBox(master=scroll, text=label, variable=var)
            cb.pack(anchor='w', padx=8, pady=4)

            self._cobros_check_vars[fid] = var
            self._cobros_facturas_map[fid] = {
                'id_cliente': id_cliente,
                'monto': monto,
                'detalles': detalles
            }

        # Controles inferiores: seleccionar todo, método de pago, ejecutar
        controles = ctk.CTkFrame(main, fg_color='white')
        controles.grid(row=2, column=0, sticky='ew', padx=10, pady=(5,10))

        # Seleccionar todo
        sel_all_var = tk.BooleanVar(value=False)

        def _toggle_all():
            v = sel_all_var.get()
            for var in self._cobros_check_vars.values():
                var.set(v)

        sel_all_cb = ctk.CTkCheckBox(master=controles, text='Seleccionar todo', variable=sel_all_var, command=_toggle_all)
        sel_all_cb.grid(row=0, column=0, sticky='w', padx=(0,10))

        # Metodo de pago
        ctk.CTkLabel(controles, text='Método de Pago:', font=("Lato Light", 12)).grid(row=0, column=1, padx=(10,5))
        metodo_cb = ctk.CTkComboBox(controles, values=['Efectivo', 'Transferencia', 'Tarjeta', 'MercadoPago', 'Otro'], width=180)
        metodo_cb.set('Efectivo')
        metodo_cb.grid(row=0, column=2, padx=(0,10))

        ejecutar_btn = ctk.CTkButton(controles, text='Ejecutar Cobros', fg_color='#E57819', command=lambda: self._ejecutar_cobros_masivos(metodo_cb.get()))
        ejecutar_btn.grid(row=0, column=3, padx=(10,0))

    def _ejecutar_cobros_masivos(self, metodo):
        """Procesa los cobros seleccionados: crea registros en 'pagos' y actualiza 'facturas' a pagada."""
        seleccionadas = [fid for fid, var in self._cobros_check_vars.items() if var.get()]
        if not seleccionadas:
            CTkMessagebox(title='Aviso', message='No hay facturas seleccionadas', icon='info')
            return

        exitos = 0
        fallos = []

        for fid in seleccionadas:
            info = self._cobros_facturas_map.get(fid)
            if not info:
                fallos.append((fid, 'info no disponible'))
                continue

            pago_data = {
                'id_factura': fid,
                'id_cliente': info['id_cliente'],
                'monto': info['monto'],
                'metodo': metodo,
                'fecha': datetime.now().strftime('%Y-%m-%d')
            }

            try:
                created = self.gestor.create('pagos', pago_data)
                if created:
                    updated = self.gestor.update('facturas', {'id_factura': fid, 'estado': 'pagada'})
                    if updated:
                        exitos += 1
                    else:
                        fallos.append((fid, 'no se pudo actualizar factura'))
                else:
                    fallos.append((fid, 'no se pudo crear pago'))
            except Exception as e:
                fallos.append((fid, str(e)))

        mensaje = f'Cobros procesados: {exitos}'
        if fallos:
            mensaje += f'. Fallos: {len(fallos)}. Detalles: ' + ', '.join([f"#{f[0]}:{f[1]}" for f in fallos])

        CTkMessagebox(title='Resultado Cobros Masivos', message=mensaje, icon='info')

        # Volver a cargar la vista para refrescar la lista
        self.cobros_masivos()

    def automatizacion_suspension_reconexion(self):
        # Interfaz para configurar y ejecutar reglas automáticas de suspensión/reconexión
        for w in self.content_frame.winfo_children():
            w.destroy()

        self.gestor = GestorCampos()

        frame = ctk.CTkFrame(self.content_frame, fg_color='white')
        frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

        ctk.CTkLabel(frame, text='Automatización: suspensión / reconexión', font=("Lato Light", 16, 'bold')).grid(row=0, column=0, sticky='w', padx=10, pady=(6,12))

        # Parámetros
        ctk.CTkLabel(frame, text='Días de vencimiento para suspender:', font=("Lato Light", 12)).grid(row=1, column=0, sticky='w', padx=10)
        self._auto_days_entry = ctk.CTkEntry(frame, width=120)
        self._auto_days_entry.insert(0, '30')
        self._auto_days_entry.grid(row=1, column=1, padx=10, pady=6, sticky='w')

        self._auto_reconnect_var = tk.BooleanVar(value=True)
        ctk.CTkCheckBox(frame, text='Reconectar automáticamente cuando no haya facturas pendientes', variable=self._auto_reconnect_var).grid(row=2, column=0, columnspan=2, sticky='w', padx=10, pady=6)

        ctk.CTkLabel(frame, text='(La reconexión buscará clientes sin facturas pendientes y los marcará como activos)', font=("Lato Light", 10)).grid(row=3, column=0, columnspan=2, sticky='w', padx=10, pady=(0,8))

        # Botones
        btn_frame = ctk.CTkFrame(frame, fg_color='transparent')
        btn_frame.grid(row=4, column=0, columnspan=2, sticky='w', padx=10, pady=(8,0))

        ctk.CTkButton(btn_frame, text='Ejecutar ahora', fg_color='#E57819', command=self._run_automation).pack(side='left', padx=(0,8))
        ctk.CTkButton(btn_frame, text='Refrescar vista', command=self.automatizacion_suspension_reconexion).pack(side='left')

        # Información / resultado
        self._auto_result_text = ctk.CTkLabel(frame, text='', font=("Lato Light", 12), wraplength=900, text_color='black')
        self._auto_result_text.grid(row=5, column=0, columnspan=2, sticky='w', padx=10, pady=(12,0))

    def _run_automation(self):
        """Ejecuta la rutina de suspensión y reconexión según parámetros ingresados."""
        days_str = self._auto_days_entry.get().strip()
        try:
            days = int(days_str)
            if days < 0:
                raise ValueError()
        except Exception:
            CTkMessagebox(title='Error', message='Ingrese un número válido de días (entero positivo).', icon='cancel')
            return

        auto_reconnect = bool(self._auto_reconnect_var.get())
        hoy = datetime.now().date()

        # Buscar facturas pendientes y agrupar por cliente
        try:
            facturas = self.gestor.read('facturas', where={'estado': 'pendiente'})
        except Exception as e:
            CTkMessagebox(title='Error', message=f'Error al leer facturas: {e}', icon='cancel')
            return

        clientes_a_suspender = set()
        for f in facturas:
            # f: (id_factura, id_cliente, fecha_emision, fecha_vencimiento, monto_total, estado, detalles)
            try:
                fecha_vto_str = f[3]
                fecha_vto = datetime.strptime(fecha_vto_str, '%Y-%m-%d').date()
            except Exception:
                # si el formato no coincide, saltar
                continue

            dias_vencidos = (hoy - fecha_vto).days
            if dias_vencidos >= days:
                clientes_a_suspender.add(f[1])

        suspendidos = 0
        cuentas_actualizadas = 0

        for id_cliente in clientes_a_suspender:
            # Actualizar estado del cliente a 'suspendido' si no lo está
            try:
                cli = self.gestor.read('cliente', where={'id_cliente': id_cliente})
                if cli:
                    estado_actual = cli[0][6] if len(cli[0]) > 6 else None
                    # intentar actualizar
                    if estado_actual != 'suspendido':
                        ok = self.gestor.update('cliente', {'id_cliente': id_cliente, 'estado_servicio': 'suspendido'})
                        if ok:
                            suspendidos += 1

                # Actualizar o crear cuenta_corriente
                cc = self.gestor.read('cuenta_corriente', where={'id_cliente': id_cliente})
                # Calcular deuda acumulada como suma de facturas pendientes
                pendientes = [ff for ff in facturas if ff[1] == id_cliente]
                deuda = sum([p[4] or 0 for p in pendientes])

                if cc:
                    id_cuenta = cc[0][0]
                    ok2 = self.gestor.update('cuenta_corriente', {'id_cuenta': id_cuenta, 'deuda_acumulada': deuda, 'estado_corte': 'cortado', 'fecha_ultimo_cambio_estado': hoy.strftime('%Y-%m-%d')})
                    if ok2:
                        cuentas_actualizadas += 1
                else:
                    # crear nueva cuenta_corriente
                    ok2 = self.gestor.create('cuenta_corriente', {'id_cliente': id_cliente, 'deuda_acumulada': deuda, 'estado_corte': 'cortado', 'fecha_ultimo_cambio_estado': hoy.strftime('%Y-%m-%d')})
                    if ok2:
                        cuentas_actualizadas += 1

            except Exception as e:
                # continuar con siguiente cliente
                continue

        reconectados = 0
        if auto_reconnect:
            # Buscar clientes que estén suspendidos/cortados y no tengan facturas pendientes
            try:
                # Obtener todos los clientes con estado distinto de 'activo'
                clientes = self.gestor.read('cliente', where={})
            except Exception as e:
                CTkMessagebox(title='Error', message=f'Error al leer clientes: {e}', icon='cancel')
                return

            for c in clientes:
                cid = c[0]
                estado_serv = c[6] if len(c) > 6 else None
                if estado_serv in ('suspendido', 'cortado', 'reconexion_pendiente'):
                    pendientes_cliente = self.gestor.read('facturas', where={'id_cliente': cid, 'estado': 'pendiente'})
                    if not pendientes_cliente:
                        # reconectar
                        okr = self.gestor.update('cliente', {'id_cliente': cid, 'estado_servicio': 'activo'})
                        if okr:
                            reconectados += 1
                        # actualizar cuenta_corriente si existe
                        cc = self.gestor.read('cuenta_corriente', where={'id_cliente': cid})
                        if cc:
                            id_cuenta = cc[0][0]
                            self.gestor.update('cuenta_corriente', {'id_cuenta': id_cuenta, 'deuda_acumulada': 0, 'estado_corte': 'al_dia', 'fecha_ultimo_cambio_estado': hoy.strftime('%Y-%m-%d')})

        resultado = f'Suspensiones aplicadas: {suspendidos}. Cuentas actualizadas: {cuentas_actualizadas}. Reconexiones automáticas: {reconectados}.'
        self._auto_result_text.configure(text=resultado)
        CTkMessagebox(title='Resultado Automatización', message=resultado, icon='info')

    def reportes_estadisticas(self):
        """Placeholder para reportes y estadísticas de pagos.
        Muestra un mensaje simple dentro del content_frame.
        """
        for w in self.content_frame.winfo_children():
            w.destroy()
        frame = ctk.CTkFrame(self.content_frame, fg_color='white')
        frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        ctk.CTkLabel(frame, text='Reportes y Estadísticas', font=("Lato Light", 16)).pack(padx=10, pady=10)
        ctk.CTkLabel(frame, text='Próximamente: gráficos de recaudación, morosidad y rendimiento por pasarela.', wraplength=800).pack(padx=10, pady=(0,10))

    def gestion_pasarelas(self):
        # Limpiar contenido previo
        for w in self.content_frame.winfo_children():
            w.destroy()

        self.gestor = GestorCampos()

        cont = ctk.CTkFrame(self.content_frame, fg_color='white')
        cont.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

        ctk.CTkLabel(cont, text='Pasarelas de Pago', font=("Lato Light", 18, 'bold')).grid(row=0, column=0, sticky='w')

        list_frame = ctk.CTkScrollableFrame(cont, fg_color='white', height=300)
        list_frame.grid(row=1, column=0, sticky='nsew', pady=(10,10))

        # Cabecera con botones
        acciones_frame = ctk.CTkFrame(cont, fg_color='white')
        acciones_frame.grid(row=2, column=0, sticky='ew')

        btn_nueva = ctk.CTkButton(acciones_frame, text='Nueva Pasarela', fg_color='#E57819', command=lambda: PasarelaEditor(self, None))
        btn_nueva.pack(side='left', padx=(0,8))

        btn_refrescar = ctk.CTkButton(acciones_frame, text='Refrescar', command=self.gestion_pasarelas)
        btn_refrescar.pack(side='left')

        # Cargar pasarelas desde DB
        try:
            pasarelas = self.gestor.read('pasarelas_pago', where={})
        except Exception as e:
            CTkMessagebox(title='Error', message=f'Error al leer pasarelas: {e}', icon='cancel')
            return

        if not pasarelas:
            ctk.CTkLabel(list_frame, text='No hay pasarelas configuradas.', font=("Lato Light", 14)).pack(padx=8, pady=8)
            return

        # Mostrar cada pasarela con acciones
        for p in pasarelas:
            # p: (id_pasarela, nombre, proveedor, api_key, api_secret, modo_prueba, activo, configuracion, fecha_creacion)
            pid = p[0]
            nombre = p[1]
            proveedor = p[2]
            activo = bool(p[6]) if len(p) > 6 else True

            row = ctk.CTkFrame(list_frame, fg_color='white')
            row.pack(fill='x', padx=6, pady=6)

            titulo = f"{nombre} — {proveedor}"
            lbl = ctk.CTkLabel(row, text=titulo, font=("Lato Light", 12, 'bold'))
            lbl.pack(side='left', padx=(6,12))

            estado_lbl = ctk.CTkLabel(row, text='Activo' if activo else 'Inactivo', text_color='green' if activo else 'red')
            estado_lbl.pack(side='left', padx=(0,12))

            def _editar(pid=pid):
                PasarelaEditor(self, pid)

            def _borrar(pid=pid, nombre=nombre):
                confirmar = CTkMessagebox(title='Confirmar', message=f'¿Eliminar pasarela {nombre}?', option_1='Cancelar', option_2='Eliminar', icon='warning')
                if confirmar.get() == 'Eliminar':
                    if self.gestor.delete('pasarelas_pago', {'id_pasarela': pid}):
                        CTkMessagebox(title='Éxito', message='Pasarela eliminada', icon='check')
                        self.gestion_pasarelas()
                    else:
                        CTkMessagebox(title='Error', message='No se pudo eliminar', icon='cancel')

            def _toggle(pid=pid, current=activo):
                nuevo = 0 if current else 1
                ok = self.gestor.update('pasarelas_pago', {'id_pasarela': pid, 'activo': nuevo})
                if ok:
                    self.gestion_pasarelas()

            ctk.CTkButton(row, text='Editar', width=90, command=_editar).pack(side='right', padx=6)
            ctk.CTkButton(row, text='Eliminar', width=90, fg_color='#E74C3C', hover_color='#C0392B', command=_borrar).pack(side='right', padx=6)
            ctk.CTkButton(row, text='Activar/Desactivar', width=140, command=_toggle).pack(side='right', padx=6)


class PasarelaEditor(ctk.CTkToplevel):
    """Toplevel simple para crear o editar pasarelas de pago."""
    def __init__(self, parent: 'PagoFrame', pasarela_id: int | None):
        super().__init__(parent)
        self.parent = parent
        self.pasarela_id = pasarela_id
        self.gestor = GestorCampos()
        self.title('Pasarela de Pago')
        self.attributes('-topmost', True)
        self.resizable(False, False)

        self._crear_ui()

        if pasarela_id:
            self._cargar(pasarela_id)

    def _crear_ui(self):
        frm = ctk.CTkFrame(self)
        frm.pack(padx=12, pady=12)

        ctk.CTkLabel(frm, text='Nombre:', anchor='w').grid(row=0, column=0, sticky='w')
        self.nombre_entry = ctk.CTkEntry(frm, width=300)
        self.nombre_entry.grid(row=0, column=1, pady=6)

        ctk.CTkLabel(frm, text='Proveedor:', anchor='w').grid(row=1, column=0, sticky='w')
        self.proveedor_entry = ctk.CTkEntry(frm, width=300)
        self.proveedor_entry.grid(row=1, column=1, pady=6)

        ctk.CTkLabel(frm, text='API Key:', anchor='w').grid(row=2, column=0, sticky='w')
        self.api_key_entry = ctk.CTkEntry(frm, width=300)
        self.api_key_entry.grid(row=2, column=1, pady=6)

        ctk.CTkLabel(frm, text='API Secret:', anchor='w').grid(row=3, column=0, sticky='w')
        self.api_secret_entry = ctk.CTkEntry(frm, width=300)
        self.api_secret_entry.grid(row=3, column=1, pady=6)

        self.modo_prueba_var = tk.BooleanVar(value=True)
        ctk.CTkCheckBox(frm, text='Modo Prueba', variable=self.modo_prueba_var).grid(row=4, column=0, columnspan=2, sticky='w', pady=6)

        self.activo_var = tk.BooleanVar(value=True)
        ctk.CTkCheckBox(frm, text='Activo', variable=self.activo_var).grid(row=5, column=0, columnspan=2, sticky='w', pady=6)

        btn_frame = ctk.CTkFrame(frm, fg_color='transparent')
        btn_frame.grid(row=6, column=0, columnspan=2, pady=(10,0))

        ctk.CTkButton(btn_frame, text='Guardar', fg_color='#E57819', command=self._guardar).pack(side='left', padx=(0,8))
        ctk.CTkButton(btn_frame, text='Cancelar', command=self.destroy).pack(side='left')

    def _cargar(self, pid: int):
        datos = self.gestor.read('pasarelas_pago', where={'id_pasarela': pid})
        if not datos:
            CTkMessagebox(title='Error', message='Pasarela no encontrada', icon='cancel')
            self.destroy()
            return
        d = datos[0]
        # (id_pasarela, nombre, proveedor, api_key, api_secret, modo_prueba, activo, configuracion, fecha_creacion)
        self.nombre_entry.insert(0, d[1])
        self.proveedor_entry.insert(0, d[2])
        self.api_key_entry.insert(0, d[3] or '')
        self.api_secret_entry.insert(0, d[4] or '')
        self.modo_prueba_var.set(bool(d[5]))
        self.activo_var.set(bool(d[6]))

    def _guardar(self):
        nombre = self.nombre_entry.get().strip()
        proveedor = self.proveedor_entry.get().strip()
        api_key = self.api_key_entry.get().strip() or None
        api_secret = self.api_secret_entry.get().strip() or None
        modo = 1 if self.modo_prueba_var.get() else 0
        activo = 1 if self.activo_var.get() else 0

        if not nombre or not proveedor:
            CTkMessagebox(title='Error', message='Nombre y proveedor son obligatorios', icon='cancel')
            return

        data = {
            'nombre': nombre,
            'proveedor': proveedor,
            'api_key': api_key,
            'api_secret': api_secret,
            'modo_prueba': modo,
            'activo': activo
        }

        if self.pasarela_id:
            data['id_pasarela'] = self.pasarela_id
            ok = self.gestor.update('pasarelas_pago', data)
        else:
            ok = self.gestor.create('pasarelas_pago', data)

        if ok:
            CTkMessagebox(title='Éxito', message='Pasarela guardada', icon='check')
            self.destroy()
            # refrescar la vista principal
            if hasattr(self.parent, 'gestion_pasarelas'):
                self.parent.gestion_pasarelas()
        else:
            CTkMessagebox(title='Error', message='No se pudo guardar la pasarela', icon='cancel')

from db.db_utils import conexion_cursor

class GestorTablas:
    def __init__(self, nombre_bd: str = "BBDDAVE.db") -> None:
        self.nombre_bd = nombre_bd

    def create_tables(self) -> None:
        with conexion_cursor(self.nombre_bd) as (conexion, cursor):
            tables_dict: dict[str, str] = {
                "cliente": """
                    CREATE TABLE IF NOT EXISTS cliente (
                        id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
                        dni TEXT UNIQUE NOT NULL,
                        nombre TEXT NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        telefono TEXT,
                        direccion TEXT NOT NULL,
                        fecha_alta DATE NOT NULL,
                        fecha_baja DATE NULL,
                        estado_servicio TEXT NOT NULL CHECK(estado_servicio IN ('activo', 'suspendido', 'cortado', 'baja'))
                    )
                """,
                "empleado": """
                    CREATE TABLE IF NOT EXISTS empleado (
                        id_empleado INTEGER PRIMARY KEY AUTOINCREMENT,
                        dni TEXT UNIQUE NOT NULL,
                        nombre TEXT NOT NULL,
                        email TEXT NOT NULL,
                        telefono TEXT NOT NULL,
                        direccion TEXT NOT NULL,
                        zona_trabajo TEXT NOT NULL,
                        fecha_ingreso DATE NOT NULL,
                        estado TEXT NOT NULL CHECK(estado IN ('activo', 'suspendido', 'baja')),
                        ultimo_acceso DATETIME,
                        contrasena TEXT NOT NULL,
                        id_rol_base INTEGER NOT NULL,
                        FOREIGN KEY (id_rol_base) REFERENCES rol_base(id_rol_base)
                    )
                """,
                "planes_servicio": """
                    CREATE TABLE IF NOT EXISTS planes_servicio (
                        id_plan INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre_plan TEXT NOT NULL,
                        velocidad_descarga INTEGER NOT NULL,
                        velocidad_subida INTEGER NOT NULL,
                        precio REAL NOT NULL,
                        tipo_conexion TEXT NOT NULL CHECK(tipo_conexion IN ('fibra', 'inalambrico', 'satelital'))
                    )
                """,
                "rol_base": """
                    CREATE TABLE IF NOT EXISTS rol_base (
                        id_rol_base INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT NOT NULL CHECK(nombre IN ('tecnico', 'secretario', 'administrador')),
                        gestion_clientes BOOLEAN NOT NULL DEFAULT 0,
                        gestion_soporte BOOLEAN NOT NULL DEFAULT 0,
                        gestion_empleados BOOLEAN NOT NULL DEFAULT 0,
                        gestion_pago BOOLEAN NOT NULL DEFAULT 0,
                        gestion_equipos BOOLEAN NOT NULL DEFAULT 0
                    )
                """,
                "auditoria_accesos": """
                    CREATE TABLE IF NOT EXISTS auditoria_accesos (
                        id_auditoria INTEGER PRIMARY KEY AUTOINCREMENT,
                        id_empleado INTEGER NOT NULL,
                        accion_realizada TEXT NOT NULL,
                        fecha_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (id_empleado) REFERENCES empleado(id_empleado)
                    )
                """,
                "servicios_contratados": """
                    CREATE TABLE IF NOT EXISTS servicios_contratados (
                        id_servicio INTEGER PRIMARY KEY AUTOINCREMENT,
                        id_cliente INTEGER NOT NULL,
                        id_plan INTEGER NOT NULL,
                        fecha_inicio DATE NOT NULL,
                        fecha_fin DATE,
                        estado_servicio TEXT NOT NULL CHECK(estado_servicio IN ('activo', 'suspendido', 'cancelado')),
                        estado_contrato TEXT NOT NULL CHECK(estado_contrato IN ('firmado', 'pendiente', 'vencido')),
                        fecha_firma DATE,
                        fecha_vencimiento DATE,
                        latitud_instalacion REAL,
                        longitud_instalacion REAL,
                        direccion_instalacion TEXT NOT NULL,
                        nodo_conexion TEXT,
                        numero_caja TEXT,
                        conexion_caja TEXT,
                        nombre_emisor TEXT,
                        FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente),
                        FOREIGN KEY (id_plan) REFERENCES planes_servicio(id_plan)
                    )
                """,
                "equipos": """
                    CREATE TABLE IF NOT EXISTS equipos (
                        id_equipo INTEGER PRIMARY KEY AUTOINCREMENT,
                        id_cliente INTEGER NOT NULL,
                        tipo_equipo TEXT NOT NULL CHECK(tipo_equipo IN ('router', 'ont', 'antena', 'modem')),
                        marca TEXT NOT NULL,
                        modelo TEXT NOT NULL,
                        serie TEXT UNIQUE NOT NULL,
                        fecha_instalacion DATE NOT NULL,
                        estado TEXT NOT NULL CHECK(estado IN ('activo', 'inactivo', 'defectuoso', 'en_mantenimiento')),
                        FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente)
                    )
                """,
                "estado_equipos": """
                    CREATE TABLE IF NOT EXISTS estado_equipos (
                        id_estado INTEGER PRIMARY KEY AUTOINCREMENT,
                        id_equipo INTEGER NOT NULL,
                        estado_conexion TEXT NOT NULL CHECK(estado_conexion IN ('online', 'offline', 'inestable')),
                        fecha_verificacion DATETIME DEFAULT CURRENT_TIMESTAMP,
                        ancho_banda_descarga REAL,
                        ancho_banda_subida REAL,
                        FOREIGN KEY (id_equipo) REFERENCES equipos(id_equipo)
                    )
                """,
                "tickets_soporte": """
                    CREATE TABLE IF NOT EXISTS tickets_soporte (
                        id_ticket INTEGER PRIMARY KEY AUTOINCREMENT,
                        id_cliente INTEGER NOT NULL,
                        id_empleado_asignado INTEGER,
                        titulo TEXT NOT NULL,
                        descripcion TEXT NOT NULL,
                        tipo_problema TEXT NOT NULL CHECK(tipo_problema IN ('conexion', 'facturacion', 'configuracion', 'tecnico', 'otros')),
                        prioridad TEXT NOT NULL CHECK(prioridad IN ('urgente', 'normal', 'baja')),
                        estado TEXT NOT NULL CHECK(estado IN ('abierto', 'en_proceso', 'cerrado', 'cancelado')),
                        fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
                        fecha_cierre DATETIME,
                        solucion TEXT,
                        FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente),
                        FOREIGN KEY (id_empleado_asignado) REFERENCES empleado(id_empleado)
                    )
                """,
                "visitas_tecnicas": """
                    CREATE TABLE IF NOT EXISTS visitas_tecnicas (
                        id_visita INTEGER PRIMARY KEY AUTOINCREMENT,
                        id_ticket INTEGER NOT NULL,
                        id_tecnico INTEGER NOT NULL,
                        fecha_programada DATETIME NOT NULL,
                        fecha_realizacion DATETIME,
                        estado TEXT NOT NULL CHECK(estado IN ('programada', 'en_camino', 'realizada', 'cancelada')),
                        observaciones TEXT,
                        FOREIGN KEY (id_ticket) REFERENCES tickets_soporte(id_ticket),
                        FOREIGN KEY (id_tecnico) REFERENCES empleado(id_empleado)
                    )
                """,
                "facturas": """
                    CREATE TABLE IF NOT EXISTS facturas (
                        id_factura INTEGER PRIMARY KEY AUTOINCREMENT,
                        id_cliente INTEGER NOT NULL,
                        fecha_emision DATE NOT NULL,
                        fecha_vencimiento DATE NOT NULL,
                        monto_total REAL NOT NULL,
                        estado TEXT NOT NULL CHECK(estado IN ('pendiente', 'pagada', 'vencida', 'cancelada')),
                        detalles TEXT,
                        FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente)
                    )
                """,
                "pagos": """
                    CREATE TABLE IF NOT EXISTS pagos (
                        id_pago INTEGER PRIMARY KEY AUTOINCREMENT,
                        id_factura INTEGER NOT NULL,
                        id_cliente INTEGER NOT NULL,
                        monto_pagado REAL NOT NULL,
                        fecha_pago DATETIME DEFAULT CURRENT_TIMESTAMP,
                        metodo_pago TEXT NOT NULL CHECK(metodo_pago IN ('transferencia', 'tarjeta', 'efectivo', 'mercadopago', 'paypal')),
                        comprobante TEXT,
                        FOREIGN KEY (id_factura) REFERENCES facturas(id_factura),
                        FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente)
                    )
                """,
                "notificaciones": """
                    CREATE TABLE IF NOT EXISTS notificaciones (
                        id_notificacion INTEGER PRIMARY KEY AUTOINCREMENT,
                        id_cliente INTEGER,
                        id_empleado INTEGER,
                        tipo TEXT NOT NULL CHECK(tipo IN ('factura', 'corte', 'reconexion', 'visita', 'ticket', 'interno')),
                        asunto TEXT NOT NULL,
                        mensaje TEXT NOT NULL,
                        fecha_envio DATETIME DEFAULT CURRENT_TIMESTAMP,
                        estado TEXT NOT NULL CHECK(estado IN ('enviado', 'pendiente', 'fallido')),
                        FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente),
                        FOREIGN KEY (id_empleado) REFERENCES empleado(id_empleado)
                    )
                """,
                "evaluaciones": """
                    CREATE TABLE IF NOT EXISTS evaluaciones (
                        id_evaluacion INTEGER PRIMARY KEY AUTOINCREMENT,
                        id_ticket INTEGER NOT NULL,
                        calificacion INTEGER NOT NULL CHECK(calificacion >= 1 AND calificacion <= 5),
                        comentarios TEXT,
                        fecha_evaluacion DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (id_ticket) REFERENCES tickets_soporte(id_ticket)
                    )
                """,
                "cuenta_corriente": """
                    CREATE TABLE IF NOT EXISTS cuenta_corriente (
                        id_cuenta INTEGER PRIMARY KEY AUTOINCREMENT,
                        id_cliente INTEGER NOT NULL UNIQUE,
                        deuda_acumulada REAL NOT NULL DEFAULT 0,
                        estado_corte TEXT NOT NULL CHECK(estado_corte IN ('al_dia', 'corte_pendiente', 'cortado', 'reconexion_pendiente')) DEFAULT 'al_dia',
                        fecha_ultimo_cambio_estado DATE,
                        FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente)
                    )
                """
                ,
                "pasarelas_pago": """
                    CREATE TABLE IF NOT EXISTS pasarelas_pago (
                        id_pasarela INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT NOT NULL UNIQUE,
                        proveedor TEXT NOT NULL,
                        api_key TEXT,
                        api_secret TEXT,
                        modo_prueba BOOLEAN NOT NULL DEFAULT 1,
                        activo BOOLEAN NOT NULL DEFAULT 1,
                        configuracion TEXT,
                        fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """
            }
            
            for table_name, create_query in tables_dict.items():
                try:
                    cursor.execute(create_query)
                    print(f"\nTabla '{table_name}' creada o ya existía.")
                except Exception as e:
                    print(f"\nError creando la tabla '{table_name}': {e}")
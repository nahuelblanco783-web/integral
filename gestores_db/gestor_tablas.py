from gestores_db.db_utils import conexion_cursor

class GestorTablas:
    def __init__(self, nombre_bd: str = "BBDDAVE.db") -> None:
        self.nombre_bd = nombre_bd

    def create_tables(self) -> None:
        with conexion_cursor(self.nombre_bd) as (conexion, cursor):
            tables_dict: dict[str, str] = {
                "cliente": """
                    CREATE TABLE IF NOT EXISTS cliente (
                        id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
                        dni NUMBER UNIQUE NOT NULL,
                        nombre TEXT NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        telefono TEXT,
                        direccion TEXT NOT NULL,
                        fecha_alta DATE NOT NULL,
                        fecha_baja DATE NULL,
                        estado BOOLEAN NOT NULL CHECK (estado IN (0, 1)) DEFAULT 1,

                    )
                """,
                "empleado": """
                    CREATE TABLE IF NOT EXISTS empleado (
                        id_empleado INTEGER PRIMARY KEY AUTOINCREMENT,
                        dni NUMBER UNIQUE NOT NULL,
                        nombre TEXT NOT NULL,
                        email TEXT NOT NULL,
                        telefono TEXT NOT NULL,
                        direccion TEXT NOT NULL,
                        rol_base TEXT NOT NULL,
                        zona_trabajo TEXT NOT NULL,
                        fecha_alta DATE NOT NULL,
                        fecha_baja DATE NULL,
                        estado BOOLEAN NOT NULL CHECK (estado IN (0, 1)) DEFAULT 1
                    )
                """,
                "planes_servicio": """
                    CREATE TABLE IF NOT EXISTS planes_servicio (
                        id_plan INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre_plan TEXT NOT NULL,
                        velocidad_descarga REAL NOT NULL,
                        velocidad_subida REAL NOT NULL,
                        precio REAL NOT NULL,
                        tipo_conexion TEXT NOT NULL,
                        descripcion TEXT
                    )
                """,
                
            }
            for table_name, create_query in tables_dict.items():
                try:
                    cursor.execute(create_query)
                    print(f"\nTabla '{table_name}' creada o ya existía.")
                except Exception as e:
                    print(f"\nError creando la tabla '{table_name}': {e}")
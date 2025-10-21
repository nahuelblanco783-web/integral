from typing import Any
from db.db_utils import conexion_cursor

class GestorCampos:
    def __init__(self, nombre_bd: str = "BBDDAVE.db") -> None:
        self.nombre_bd = nombre_bd

    def _obtener_columnas(self, table: str) -> list[dict[str, Any]]:
        """Devuelve info completa de las columnas: nombre, tipo, si es PK, etc."""
        with conexion_cursor(self.nombre_bd) as (_conn, cursor):
            cursor.execute(f"PRAGMA table_info({table})")
            columnas_info = cursor.fetchall()

        columnas = []
        for col in columnas_info:
            columnas.append({
                "name": col[1],
                "type": col[2].upper() if col[2] else "",
                "pk": bool(col[5])
            })
        return columnas

    def create(self, table: str, values: list[Any] | dict[str, Any]) -> bool:
        """
        Inserta un registro en la tabla indicada.
        - Si se pasa una lista: se asume orden según columnas (NO RECOMENDADO si hay campos opcionales).
        - Si se pasa un dict: se insertan solo las columnas especificadas.
        - Respeta DEFAULT y NULL según corresponda.
        """
        try:
            # Obtener info de columnas extendida
            with conexion_cursor(self.nombre_bd) as (_conn, cursor):
                cursor.execute(f"PRAGMA table_xinfo({table})")
                columnas_ext = cursor.fetchall()

            columnas_insertables = [
                c for c in columnas_ext
                if not (c[5] == 1 and "INT" in (c[2] or "").upper())  # evitar PK INT AUTOINCREMENT
            ]

            columnas_nombres = [c[1] for c in columnas_insertables]
            columnas_not_null = {c[1] for c in columnas_insertables if c[3] == 1 and c[4] is None}

            # --- Caso 1: Diccionario ---
            if isinstance(values, dict):
                # Validar que no falten columnas NOT NULL sin default
                faltantes = columnas_not_null - set(values.keys())
                if faltantes:
                    raise ValueError(f"Faltan columnas obligatorias (NOT NULL sin default): {faltantes}")

                columnas_a_insertar = list(values.keys())
                valores_a_insertar = list(values.values())

            # --- Caso 2: Lista ---
            else:
                if len(values) > len(columnas_nombres):
                    raise ValueError(f"Demasiados valores ({len(values)}) para columnas ({len(columnas_nombres)})")

                # Rellenar con None solo si faltan valores
                valores_a_insertar = list(values) + [None] * (len(columnas_nombres) - len(values))
                columnas_a_insertar = columnas_nombres[:len(valores_a_insertar)]

            # Armar la query final
            keys = ', '.join(columnas_a_insertar)
            placeholders = ', '.join(['?' for _ in columnas_a_insertar])
            sql_query = f"INSERT INTO {table} ({keys}) VALUES ({placeholders})"

            with conexion_cursor(self.nombre_bd) as (conn, cursor):
                cursor.execute(sql_query, tuple(valores_a_insertar))
                conn.commit()

            return True

        except Exception as e:
            print(f"Error al insertar en {table}: {e}")
            return False

    def read(self, table: str, where: dict[str, Any] | None = None) -> list[Any]:
        sql_query = f"SELECT * FROM {table}"
        params = []
        if where:
            conditions = [f"{k}=?" for k in where.keys()]
            sql_query += " WHERE " + " AND ".join(conditions)
            params = list(where.values())
        try:
            with conexion_cursor(self.nombre_bd) as (_conn, cursor):
                cursor.execute(sql_query, params)
                return cursor.fetchall()
        except Exception as e:
            print(f"Error al leer de {table}: {e}")
            return []

    def update(self, table: str, values: list[Any]) -> bool:
        """
        Actualiza un registro usando solo una lista de valores.
        La última posición de la lista corresponde al valor de la clave primaria.
        """
        try:
            columnas_info = self._obtener_columnas(table)
            pk_col = next((c["name"] for c in columnas_info if c["pk"]), None)
            if pk_col is None:
                raise ValueError(f"La tabla {table} no tiene clave primaria definida.")

            columnas = [c["name"] for c in columnas_info if c["name"] != pk_col]
            if len(values) != len(columnas) + 1:
                raise ValueError(
                    f"La cantidad de valores ({len(values)}) no coincide con columnas+PK ({len(columnas) + 1}): {columnas + [pk_col]}"
                )

            set_clause = ', '.join([f"{col}=?" for col in columnas])
            sql_query = f"UPDATE {table} SET {set_clause} WHERE {pk_col}=?"

            params = values  # valores + pk al final
            with conexion_cursor(self.nombre_bd) as (conn, cursor):
                cursor.execute(sql_query, tuple(params))
                conn.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar en {table}: {e}")
            return False

    def delete(self, table: str, where: dict[str, Any]) -> bool:
        where_clause = ' AND '.join([f"{k}=?" for k in where.keys()])
        sql_query = f"DELETE FROM {table} WHERE {where_clause}"
        params = list(where.values())
        try:
            with conexion_cursor(self.nombre_bd) as (conn, cursor):
                cursor.execute(sql_query, params)
                conn.commit()
            return True
        except Exception as e:
            print(f"Error al eliminar de {table}: {e}")
            return False

    # --- Métodos específicos para campos ---
    def get_campos(self, table: str) -> list[str]:
        sql_query = f"SELECT name FROM pragma_table_info('{table}')"
        try:
            with conexion_cursor(self.nombre_bd) as (_conn, cursor):
                cursor.execute(sql_query)
                campos = [row[0] for row in cursor.fetchall()]
                # Transformar: "_" → " " y Primera letra mayúscula
                campos_formateados = [campo.replace("_", " ").title() for campo in campos]
                return campos_formateados
        except Exception as e:
            print(f"Error al obtener campos de {table}: {e}")
            return []
        
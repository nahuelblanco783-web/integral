from typing import Any
from gestores_db.db_utils import conexion_cursor

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

    def create(self, table: str, values: list[Any]) -> bool:
        """Inserta un registro en la tabla indicada usando solo una lista de valores."""
        try:
            columnas_info = self._obtener_columnas(table)
            columnas = [
                c["name"] for c in columnas_info
                if not (c["pk"] and "INT" in c["type"])
            ]

            if len(columnas) != len(values):
                raise ValueError(
                    f"La cantidad de valores ({len(values)}) no coincide con las columnas ({len(columnas)}): {columnas}"
                )

            keys = ', '.join(columnas)
            placeholders = ', '.join(['?' for _ in values])
            sql_query = f"INSERT INTO {table} ({keys}) VALUES ({placeholders})"

            with conexion_cursor(self.nombre_bd) as (conn, cursor):
                cursor.execute(sql_query, tuple(values))
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

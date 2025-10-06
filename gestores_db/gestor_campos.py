
from typing import Any
from gestores_db.db_utils import conexion_cursor

class GestorCampos:
    def __init__(self, nombre_bd: str = "BBDDAVE.db") -> None:
        self.nombre_bd = nombre_bd
    
    def create(self, table: str, values: dict[str, Any]) -> bool:
        """Inserta un registro en la tabla indicada con los valores dados."""
        keys = ', '.join(values.keys())
        placeholders = ', '.join(['?' for _ in values])
        sql_query = f"INSERT INTO {table} ({keys}) VALUES ({placeholders})"
        try:
            with conexion_cursor(self.nombre_bd) as (conn, cursor):
                cursor.execute(sql_query, tuple(values.values()))
                conn.commit()
            return True
        except Exception as e:
            print(f"Error al insertar en {table}: {e}")
            return False

    def read(self, table: str, where: dict[str, Any] | None = None) -> list[Any]:
        """Lee registros de la tabla indicada, opcionalmente filtrando por los valores dados."""
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

    def update(self, table: str, values: dict[str, Any], where: dict[str, Any]) -> bool:
        """Actualiza registros en la tabla indicada según la condición dada."""
        set_clause = ', '.join([f"{k}=?" for k in values.keys()])
        where_clause = ' AND '.join([f"{k}=?" for k in where.keys()])
        sql_query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        params = list(values.values()) + list(where.values())
        try:
            with conexion_cursor(self.nombre_bd) as (conn, cursor):
                cursor.execute(sql_query, params)
                conn.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar en {table}: {e}")
            return False

    def delete(self, table: str, where: dict[str, Any]) -> bool:
        """Elimina registros de la tabla indicada según la condición dada."""
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
    

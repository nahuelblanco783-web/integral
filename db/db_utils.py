import sqlite3 as sql
from contextlib import closing, contextmanager
from typing import Generator, Tuple, Union, Sequence

@contextmanager
def conexion_cursor(nombre_bd: str) -> Generator[Tuple[sql.Connection, sql.Cursor], None, None]:
    conexion = None
    try:
        conexion = sql.connect(nombre_bd)
        with closing(conexion.cursor()) as cursor:
            yield conexion, cursor
    except sql.Error as e:
        print(f"\nError en la conexión o cursor: {e}")
        raise
    finally:
        if conexion:
            conexion.close()

# Función auxiliar que usa un cursor ya abierto
def existe_registro(
    cursor: sql.Cursor,
    nombre_tabla: str,
    nombre_campo: str,
    valor_campo: Union[str, int, bool, None]
) -> bool:
    try:
        query = f"SELECT 1 FROM {nombre_tabla} WHERE {nombre_campo} = ?"
        cursor.execute(query, (valor_campo,))
        return cursor.fetchone() is not None
    except sql.Error as e:
        print(f"\nError verificando existencia del registro: {e}")
        return False

# Función auxiliar para corroborar que no sean numeros negativos
def validar_no_negativos(campos: Sequence[Union[int, float]]) -> bool:
    return all(x >= 0 for x in campos)
from db.gestor_tablas import GestorTablas
from db.gestor_campos import GestorCampos

gt_tablas = GestorTablas()
gt_campos = GestorCampos()

#Crear tablas
# gt_tablas.create_tables()

# # Crear campos
gt_campos.create(
    table="rol_base",
    values=[
        "administrador",
        1,
        1,
        1,
        1,
        1
    ]
)

gt_campos.create(
    table='empleado',
    values=[
        "admin",
        "Mc Gregor",
        "admin@gmail.com",
        "123456",
        "pisculichi 34",
        "secretaria",
        "2020-05-05",
        "activo",
        "0",
        "0",
        2
    ]
 )

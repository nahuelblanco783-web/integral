from db.gestor_tablas import GestorTablas
from db.gestor_campos import GestorCampos

gt_tablas = GestorTablas()
gt_campos = GestorCampos()

#Crear tablas
gt_tablas.create_tables()



# # # Crear campos
# gt_campos.create(
#     table='cliente',
#     values=[
#         "123445368",
#         "juan perez",
#         "juan3p4e3rez@gmail.com",
#         "123456",
#         "pisculichi 34",
#         "2020-06-23",
#         "activo"
#     ]
# )

gt_campos.create(
    table="empleado",
    values=[
        "12345678",
        "juan perez",
        "juanperez@gmail.com",
        "123456",
        "pisculichi 34",
        'secretario',
        "Secretaria",
        "2020-06-23",
        "activo",
        "0",
        "hola123"
    ]
)
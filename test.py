from gestores_db.gestor_tablas import GestorTablas
from gestores_db.gestor_campos import GestorCampos

gt_tablas = GestorTablas()
gt_campos = GestorCampos()

# Crear tablas
# gt_tablas.create_tables()



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

gt_campos.update(
    table="cliente",
    values=[
        "1234445368",
        "jua3n perez",
        "juan43p564e3rez@gmail.com",
        "123456",
        "pisculichi 34",
        "2020-06-23",
        "activo",
        4
    ]
)
from db.gestor_tablas import GestorTablas
from db.gestor_campos import GestorCampos

gt_tablas = GestorTablas()
gt_campos = GestorCampos()
print(
gt_campos.get_campos("cliente"))
#Crear tablas
# gt_tablas.create_tables()

# # Crear campos
# gt_campos.create(
#     table="rol_base",
#     values=[
#         "administrador",
#         1,
#         1,
#         1,
#         1,
#         1
#     ]
# )

# gt_campos.create(
#     table='empleado',
#     values=[
#         "admin",
#         "Mc Gregor",
#         "admin@gmail.com",
#         "123456",
#         "pisculichi 34",
#         "secretaria",
#         "2020-05-05",
#         "activo",
#         "0",
#         "0",
#         2
#     ]
#  )

nombres = ["Maxi", "Ana", "Juan", "Lucía", "Pedro", "Carla", "Sofía", "Matías", "Laura", "Nicolás",
           "Paula", "Mariano", "Agustina", "Gonzalo", "Camila", "Julián", "Rocío", "Valentín", "Brenda", "Ezequiel"]


for i in range(1, 41):
    dni = str(10000000 + i * 123)  # Ejemplo simple de DNI diferente
    nombre = nombres[i % len(nombres)]
    email = f"{nombre.lower()}{i}@gmail.com"
    telefono = '12'
    direccion = '123'
    fecha_alta = '2023-10-10'
    estado = 'activo'

    gt_campos.create(
        table="cliente",
        values=[
            dni,
            nombre,
            email,
            telefono,
            direccion,
            fecha_alta,
            estado,
        ]
    )
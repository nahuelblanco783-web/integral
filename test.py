from db.gestor_campos import GestorCampos
gc = GestorCampos()
# gc.create(
#     table='tickets_soporte',
#     values={
#         'id_cliente': 1,
#         'titulo': 'problema',
#         'descripcion': 'no anda el equipo',
#         'tipo_problema': 'conexion',
#         'prioridad': 'normal',
#         'estado': 'abierto'
#     }
# )
gc.create(
    table='cliente',
    values=[
        '3214',
        'juanito',
        'email@email.con',
        '55',
        'nose',
        '2025-5-5',
        'activo'
    ]
)

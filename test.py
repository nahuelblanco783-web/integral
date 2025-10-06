from gestores_db.gestor_tablas import GestorTablas
from gestores_db.gestor_campos import GestorCampos

gt_tablas = GestorTablas()
gt_campos = GestorCampos()

# Crear tablas
gt_tablas.create_tables()

# # Crear campos
# gt_campos.create_fields()
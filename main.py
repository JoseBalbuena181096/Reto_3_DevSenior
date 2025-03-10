import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importar la aplicación
from views.main_view import iniciar_aplicacion

# Iniciar la aplicación
if __name__ == "__main__":
    iniciar_aplicacion()
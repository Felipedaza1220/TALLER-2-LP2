"""
Application factory de la Tienda Virtual (versión con base de datos).
"""

import os

from flask import Flask

from config import Config
from .extensions import db


def create_app(config_class=Config):
    """Crea y configura la instancia de la aplicación Flask."""
    app = Flask(__name__)

    # Cargar la configuración
    app.config.from_object(config_class)

    # Asegura que exista la carpeta instance/
    os.makedirs(
        os.path.join(app.root_path, "..", "instance"),
        exist_ok=True
    )

    # Inicializar SQLAlchemy
    db.init_app(app)

    # Importar los modelos
    from . import models  # noqa: F401

    # Registrar las rutas
    from .routes import main
    app.register_blueprint(main)

    # Registrar los comandos personalizados
    from .commands import registrar_comandos

    registrar_comandos(app)

    return app

from flask import Flask
import logging

def chatbot():
    app = Flask(__name__)
    
    # Configurar el registro
    logging.basicConfig(level=logging.INFO)
    app.logger.setLevel(logging.INFO)

    # Cargar la configuración
    app.config.from_object('config.Config')

    # Importar y registrar las rutas
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
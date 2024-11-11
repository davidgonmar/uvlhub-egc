import os

from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_migrate import Migrate

from core.configuration.configuration import get_app_version
from core.managers.module_manager import ModuleManager
from core.managers.config_manager import ConfigManager
from core.managers.error_handler_manager import ErrorHandlerManager
from core.managers.logging_manager import LoggingManager




# The authorization URL and redirect URL must match the ones you specified when you created the OAuth client ID
AUTH_URL = 'https://accounts.google.com/o/oauth2/auth'
# Load environment variables
load_dotenv()

# Create the instances
db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name='development'):

    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

    app = Flask(__name__)

    # Configuración de la sesión
    app.config['SESSION_COOKIE_SECURE'] = False  # Cambiar a True en producción para habilitar HTTPS
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Configuración para evitar problemas de redirección con OAuth
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    # Cargar la configuración según el entorno
    config_manager = ConfigManager(app)
    config_manager.load_config(config_name=config_name)

    # Inicializar SQLAlchemy y Migrate con la aplicación
    db.init_app(app)
    migrate.init_app(app, db)

    # Registrar módulos
    module_manager = ModuleManager(app)
    module_manager.register_modules()

    # Configurar el manejador de inicio de sesión
    from flask_login import LoginManager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id):
        from app.modules.auth.models import User
        return User.query.get(int(user_id))

    # Configuración de logs
    logging_manager = LoggingManager(app)
    logging_manager.setup_logging()

    # Inicializar el manejador de errores
    error_handler_manager = ErrorHandlerManager(app)
    error_handler_manager.register_error_handlers()

    # Inyección de variables de entorno en el contexto de Jinja
    @app.context_processor
    def inject_vars_into_jinja():
        return {
            'FLASK_APP_NAME': os.getenv('FLASK_APP_NAME'),
            'FLASK_ENV': os.getenv('FLASK_ENV'),
            'DOMAIN': os.getenv('DOMAIN', 'localhost'),
            'APP_VERSION': get_app_version()
        }

    return app


app = create_app()


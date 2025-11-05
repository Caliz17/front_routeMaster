from flask import Flask
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from .config import Config
from .services.auth import AuthService
from .models.user import User

csrf = CSRFProtect()
bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id: str) -> User | None:
    return AuthService.get_session_user(user_id)

def create_app(config_class: type[Config] = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)

    csrf.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)

    from .controllers.auth import auth_bp
    from .controllers.dashboard import dashboard_bp
    from .controllers.users import users_bp
    from .controllers.productos import productos_bp
    from .controllers.clientes import clientes_bp
    from .controllers.pedidos import pedidos_bp
    from .controllers.rutas import rutas_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(productos_bp)
    app.register_blueprint(clientes_bp)
    app.register_blueprint(pedidos_bp)
    app.register_blueprint(rutas_bp)

    @app.context_processor
    def inject_globals():
        return {
            "app_name": app.config.get("APP_NAME", "RouteMaster"),
            "api_base_url": app.config.get("API_BASE_URL"),
        }

    return app

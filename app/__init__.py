from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes.clientes_routes import bp_clientes
    app.register_blueprint(bp_clientes, url_prefix='/api/clientes')

    from .routes.atendimentos_routes import bp_atendimentos
    app.register_blueprint(bp_atendimentos, url_prefix='/api/atendimentos')

    from .routes.servicos_routes import bp_servicos
    app.register_blueprint(bp_servicos, url_prefix='/api/servicos')

    from .routes.views_routes import bp_views
    app.register_blueprint(bp_views, url_prefix='/')

    from . import models

    return app
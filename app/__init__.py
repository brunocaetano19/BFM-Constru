from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # Configurações da aplicação
    app.config.from_object('config.Config')
    
    # Inicializar extensões
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Registrar blueprints
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    return app

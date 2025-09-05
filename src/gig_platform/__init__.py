from flask import Flask
from flask_migrate import Migrate
from extensions import db, csrf
from config import get_config
import os

migrate = Migrate()

def create_app(config_class=None):
    """
    Application factory function.
    
    Args:
        config_class: Configuration class to use (defaults to appropriate env config)
    
    Returns:
        Flask application instance
    """
    if config_class is None:
        config_class = get_config()
    
    app = Flask(
        __name__, 
        template_folder='templates',
        static_folder='static'
    )
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    # Register blueprints
    from .routes.main import bp as main_bp
    from .routes.jobs import bp as jobs_bp
    from .routes.workers import bp as workers_bp
    from .routes.map import bp as map_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(jobs_bp, url_prefix="/jobs")
    app.register_blueprint(workers_bp, url_prefix="/workers")
    app.register_blueprint(map_bp, url_prefix="/map")

    # Initialize database
    with app.app_context():
        db.create_all()

    return app


# Create app instance for immediate use
app = create_app()
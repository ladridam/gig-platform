from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_migrate import Migrate
import os

# Initialize extensions
db = SQLAlchemy()
csrf = CSRFProtect()
migrate = Migrate()

def create_app():
    """Simple application factory."""
    app = Flask(__name__, template_folder='templates', static_folder='static')
    
    # Basic configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///gig_platform.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)
    
    # Import and register blueprints
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

# Create app instance
app = create_app()
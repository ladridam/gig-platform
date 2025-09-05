from flask import Flask
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

# Load environment variables
if os.environ.get("RENDER") is None:
    load_dotenv()

migrate = Migrate()

def create_app(config_class="gig_platform.config.Config"):
    """Application factory function."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    from gig_platform.extensions import db, csrf

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    # Register blueprints
    from gig_platform.routes.main import bp as main_bp
    from gig_platform.routes.jobs import bp as jobs_bp
    from gig_platform.routes.workers import bp as workers_bp
    from gig_platform.routes.map import bp as map_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(jobs_bp, url_prefix="/jobs")
    app.register_blueprint(workers_bp, url_prefix="/workers")
    app.register_blueprint(map_bp, url_prefix="/map")

    # Initialize database
    with app.app_context():
        db.create_all()

    return app
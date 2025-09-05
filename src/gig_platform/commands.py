import click
from flask import current_app
from flask_migrate import Migrate
from gig_platform import create_app
# Ensure the correct import path for db; update as needed if the file/module is named differently
from gig_platform.extensions import db  # Change 'extensions' to the correct module if necessary

def get_app():
    """Get the Flask application instance."""
    return create_app()

@click.group()
def cli():
    """Gig Platform CLI."""
    pass

@cli.group()
def db():
    """Database management commands."""
    pass

@db.command()
@click.option('--directory', default='migrations', help='Migration directory')
@click.option('--multidb', is_flag=True, help='Multiple databases')
def init(directory, multidb):
    """Initialize database migrations."""
    app = get_app()
    migrate = Migrate(app, db, directory=directory)
    with app.app_context():
        migrate.init_app(app, db, directory=directory)
    click.echo(f"Migrations initialized in {directory}")

@db.command()
@click.option('--directory', default='migrations', help='Migration directory')
@click.option('--message')
def migrate(directory, message):
    """Create a migration."""
    app = get_app()
    migrate = Migrate(app, db, directory=directory)
    with app.app_context():
        migrate.migrate(message=message)
    click.echo("Migration created")

@db.command()
@click.option('--directory', default='migrations', help='Migration directory')
def upgrade(directory):
    """Apply migrations."""
    app = get_app()
    migrate = Migrate(app, db, directory=directory)
    with app.app_context():
        migrate.upgrade()
    click.echo("Migrations applied")

@db.command()
@click.option('--directory', default='migrations', help='Migration directory')
def downgrade(directory):
    """Revert migrations."""
    app = get_app()
    migrate = Migrate(app, db, directory=directory)
    with app.app_context():
        migrate.downgrade()
    click.echo("Migrations reverted")
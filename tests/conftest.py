import pytest
from gig_platform import create_app
from gig_platform.extensions import db


@pytest.fixture
def app():
    """Create application for testing."""
    app = create_app("gig_platform.config.TestingConfig")
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create CLI runner."""
    return app.test_cli_runner()
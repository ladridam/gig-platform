# Gig Platform

A Flask-based web application connecting job posters with workers. Features interactive maps, location-based searching, and real-time job/worker management.

## Features

- Job posting and management
- Worker profiles and search
- Interactive map with location markers
- Address-based location input with autocomplete
- Responsive design with Bootstrap
- RESTful API structure
- Database migrations
- Comprehensive testing

## Project Structure
gig-platform/
├── src/gig_platform/ # Application package
├── tests/ # Test suite
├── migrations/ # Database migrations
├── static/ # Static assets
└── templates/ # Jinja2 templates

## Installation

1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate venv: `source venv/bin/activate`
4. Install dependencies: `pip install -e ".[dev]"`
5. Set environment variables: `cp .env.example .env`
6. Initialize database: `flask db upgrade`
7. Run the app: `flask run`

## Development

- Run tests: `pytest`
- Format code: `black src tests`
- Lint code: `flake8 src tests`
- Type checking: `mypy src`

## Deployment

The app is ready for deployment on:
- Render
- Heroku
- PythonAnywhere
- Any WSGI-compatible hosting

## Technologies Used

- Flask
- SQLAlchemy
- Flask-Migrate
- Bootstrap
- Leaflet.js
- Geopy
- pytest

# To add new packages, update requirements with:
pip freeze > requirements.txt


gig-platform/
├── src/
│   └── gig_platform/
│       ├── __init__.py
│       ├── config.py
│       ├── extensions.py
│       ├── models/
│       │   ├── __init__.py
│       │   ├── job.py
│       │   └── worker.py
│       ├── forms/
│       │   ├── __init__.py
│       │   ├── job_form.py
│       │   └── worker_form.py
│       ├── routes/
│       │   ├── __init__.py
│       │   ├── main.py
│       │   ├── jobs.py
│       │   ├── workers.py
│       │   └── map.py
│       ├── services/
│       │   ├── __init__.py
│       │   ├── geocoding.py
│       │   └── validation.py
│       ├── utils/
│       │   ├── __init__.py
│       │   └── helpers.py
│       └── templates/ (same as current)
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_models.py
│   ├── test_routes.py
│   └── test_services.py
├── migrations/
├── instance/
├── static/ (same structure)
├── .env.example
├── .flake8
├── pyproject.toml
├── requirements.txt
└── run.py
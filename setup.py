from setuptools import setup, find_packages

setup(
    name="gig-platform",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "Flask==3.1.2",
        "Flask-SQLAlchemy==3.1.1",
        "Flask-WTF==1.2.2",
        "Flask-Migrate==4.0.5",
        "python-dotenv==1.0.1",
        "geopy==2.4.1",
        "psycopg2-binary==2.9.9",
    ],
    extras_require={
        "dev": [
            "pytest==8.3.4",
            "pytest-flask==1.3.0",
            "black==24.10.0",
            "flake8==7.1.1",
            "mypy==1.12.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "gig-platform=run:cli",
        ],
        "flask.commands": [
            "db=gig_platform.commands:db",
        ],
    },
)
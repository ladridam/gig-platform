from .main import bp as main_bp
from .jobs import bp as jobs_bp
from .workers import bp as workers_bp
from .map import bp as map_bp

__all__ = ["main_bp", "jobs_bp", "workers_bp", "map_bp"]
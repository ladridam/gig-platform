from flask import Blueprint, render_template
from gig_platform.models import Job, Worker
from gig_platform.services import normalize_data

bp = Blueprint("map", __name__)


@bp.route("/")
def map_view():
    """Interactive map view."""
    jobs = Job.query.all()
    workers = Worker.query.all()
    
    return render_template(
        "map.html",
        jobs=normalize_data(jobs),
        workers=normalize_data(workers)
    )
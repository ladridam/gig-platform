from flask import (
    Blueprint, render_template, request, redirect, 
    url_for, flash, current_app
)
from gig_platform.extensions import db
from gig_platform.models import Worker
from gig_platform.forms import WorkerForm
from gig_platform.services import (
    geocoding_service, 
    get_coordinates_from_request,
)

bp = Blueprint("workers", __name__)


@bp.route("/", methods=["GET", "POST"])
def workers():
    """Workers listing and creation."""
    form = WorkerForm()
    
    if form.validate_on_submit():
        name = form.name.data
        skill = form.skill.data
        experience = form.experience.data
        location_name = form.location.data
        
        # Get coordinates from request or geocode
        coords = get_coordinates_from_request()
        if not coords:
            coords = geocoding_service.geocode_location(location_name)
            if not coords:
                flash(
                    "Could not find that location. Please try a different address or be more specific.", 
                    "danger"
                )
                return redirect(url_for("workers.workers"))
        
        # Save to database
        try:
            new_worker = Worker(
                name=name, 
                skill=skill, 
                experience=experience, 
                lat=coords[0], 
                lng=coords[1]
            )
            db.session.add(new_worker)
            db.session.commit()
            flash("Worker added successfully!", "success")
            return redirect(url_for("workers.workers"))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error creating worker: {str(e)}")
            flash("Error creating worker. Please try again.", "danger")
    
    workers = Worker.query.all()
    return render_template("workers.html", workers=workers, form=form)


@bp.route("/<int:id>/delete", methods=["POST"])
def delete_worker(id):
    """Delete a worker."""
    try:
        worker = Worker.query.get_or_404(id)
        db.session.delete(worker)
        db.session.commit()
        flash("Worker deleted successfully", "success")
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error deleting worker {id}: {str(e)}")
        flash("Error deleting worker", "danger")
    
    return redirect(url_for("workers.workers"))
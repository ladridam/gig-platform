from flask import (
    Blueprint, render_template, request, redirect, 
    url_for, flash, current_app
)
from gig_platform.extensions import db
from gig_platform.models import Job
from gig_platform.forms import JobForm
from gig_platform.services import (
    geocoding_service, 
    get_coordinates_from_request,
)

bp = Blueprint("jobs", __name__)


@bp.route("/", methods=["GET", "POST"])
def jobs():
    """Jobs listing and creation."""
    form = JobForm()
    
    if form.validate_on_submit():
        title = form.title.data
        location_name = form.location.data
        pay = form.pay.data
        
        # Get coordinates from request or geocode
        coords = get_coordinates_from_request()
        if not coords:
            coords = geocoding_service.geocode_location(location_name)
            if not coords:
                flash(
                    "Could not find that location. Please try a different address or be more specific.", 
                    "danger"
                )
                return redirect(url_for("jobs.jobs"))
        
        # Save to database
        try:
            new_job = Job(title=title, lat=coords[0], lng=coords[1], pay=pay)
            db.session.add(new_job)
            db.session.commit()
            flash("Job added successfully!", "success")
            return redirect(url_for("jobs.jobs"))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error creating job: {str(e)}")
            flash("Error creating job. Please try again.", "danger")
    
    jobs = Job.query.all()
    return render_template("jobs.html", jobs=jobs, form=form)


@bp.route("/<int:id>/delete", methods=["POST"])
def delete_job(id):
    """Delete a job."""
    try:
        job = Job.query.get_or_404(id)
        db.session.delete(job)
        db.session.commit()
        flash("Job deleted successfully", "success")
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Error deleting job {id}: {str(e)}")
        flash("Error deleting job", "danger")
    
    return redirect(url_for("jobs.jobs"))
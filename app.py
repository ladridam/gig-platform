import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm, CSRFProtect
from flask_migrate import Migrate 
from wtforms import StringField, validators
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from dotenv import load_dotenv

if os.environ.get('Render') is None:
    load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///gig_platform.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
csrf = CSRFProtect(app)
migrate = Migrate(app, db)

# Models
class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)
    pay = db.Column(db.String(50), nullable=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "location": [self.lat, self.lng],
            "pay": self.pay
        }

class Worker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    skill = db.Column(db.String(100), nullable=False)
    experience = db.Column(db.String(50), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "skill": self.skill,
            "experience": self.experience,
            "location": [self.lat, self.lng]
        }

# Forms
class JobForm(FlaskForm):
    title = StringField('Job Title', [validators.DataRequired()])
    location = StringField('Location', [validators.DataRequired()])
    pay = StringField('Pay', [validators.DataRequired()])

class WorkerForm(FlaskForm):
    name = StringField('Name', [validators.DataRequired()])
    skill = StringField('Skill', [validators.DataRequired()])
    experience = StringField('Experience', [validators.DataRequired()])
    location = StringField('Location', [validators.DataRequired()])

# Utility functions
def geocode_location(location_name):
    """Convert location name to coordinates"""
    geolocator = Nominatim(user_agent="gig_platform")
    try:
        location = geolocator.geocode(location_name)
        if location:
            return (location.latitude, location.longitude)
        return None
    except (GeocoderTimedOut, GeocoderServiceError):
        return None

def normalize_data(data):
    """Convert database objects to dicts with list locations"""
    normalized = []
    for item in data:
        if hasattr(item, 'to_dict'):
            normalized.append(item.to_dict())
        else:
            new_item = item.copy()
            if "location" in new_item and isinstance(new_item["location"], tuple):
                new_item["location"] = list(new_item["location"])
            normalized.append(new_item)
    return normalized

# Routes
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/jobs", methods=["GET", "POST"])
def jobs():
    form = JobForm()
    
    if form.validate_on_submit():
        title = form.title.data
        location_name = form.location.data
        pay = form.pay.data
        
        # Get coordinates from hidden inputs or geocode
        lat = request.form.get("lat")
        lng = request.form.get("lng")
        
        if lat and lng:
            try:
                coords = (float(lat), float(lng))
            except ValueError:
                flash("Invalid coordinates provided", "danger")
                return redirect(url_for("jobs"))
        else:
            # Fall back to geocoding
            coords = geocode_location(location_name)
            if not coords:
                flash("Could not find that location. Please try a different address or be more specific.", "danger")
                return redirect(url_for("jobs"))
        
        # Save to database
        new_job = Job(title=title, lat=coords[0], lng=coords[1], pay=pay)
        db.session.add(new_job)
        db.session.commit()
        flash("Job added successfully!", "success")
        return redirect(url_for("jobs"))
    
    jobs = Job.query.all()
    return render_template("jobs.html", jobs=jobs, form=form)

@app.route("/delete_job/<int:id>", methods=["POST"])
def delete_job(id):
    try:
        job = Job.query.get_or_404(id)
        db.session.delete(job)
        db.session.commit()
        flash("Job deleted successfully", "success")
    except Exception as e:
        db.session.rollback()
        flash("Error deleting job", "danger")
        app.logger.error(f"Error deleting job {id}: {str(e)}")
    return redirect(url_for("jobs"))

@app.route("/workers", methods=["GET", "POST"])
def workers():
    form = WorkerForm()
    
    if form.validate_on_submit():
        name = form.name.data
        skill = form.skill.data
        experience = form.experience.data
        location_name = form.location.data
        
        # Get coordinates from hidden inputs or geocode
        lat = request.form.get("lat")
        lng = request.form.get("lng")
        
        if lat and lng:
            try:
                coords = (float(lat), float(lng))
            except ValueError:
                flash("Invalid coordinates provided", "danger")
                return redirect(url_for("workers"))
        else:
            # Fall back to geocoding
            coords = geocode_location(location_name)
            if not coords:
                flash("Could not find that location. Please try a different address or be more specific.", "danger")
                return redirect(url_for("workers"))
        
        # Save to database
        new_worker = Worker(name=name, skill=skill, experience=experience, lat=coords[0], lng=coords[1])
        db.session.add(new_worker)
        db.session.commit()
        flash("Worker added successfully!", "success")
        return redirect(url_for("workers"))
    
    workers = Worker.query.all()
    return render_template("workers.html", workers=workers, form=form)

@app.route("/delete_worker/<int:id>", methods=["POST"])
def delete_worker(id):
    worker = Worker.query.get_or_404(id)
    db.session.delete(worker)
    db.session.commit()
    flash("Worker deleted successfully", "success")
    return redirect(url_for("workers"))

@app.route("/map")
def map_view():
    jobs = Job.query.all()
    workers = Worker.query.all()
    return render_template(
        "map.html",
        jobs=normalize_data(jobs),
        workers=normalize_data(workers)
    )

# Initialize database
with app.app_context():
    db.create_all()

def find_available_port(start_port=5000, max_port=5050):
    """Find an available port in the given range"""
    import socket
    from contextlib import closing
    
    for port in range(start_port, max_port + 1):
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            try:
                sock.bind(('0.0.0.0', port))
                return port
            except OSError:
                continue
    return start_port  # Fallback

if __name__ == "__main__":
    port = int(os.environ.get("PORT", find_available_port()))
    debug = os.environ.get("FLASK_DEBUG", "False").lower() == "true" and os.environ.get('Render') is None
    app.run(host="0.0.0.0", port=port, debug=debug)
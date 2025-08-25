from flask import Flask, render_template, request, redirect, url_for
from geopy.distance import geodesic

app = Flask(__name__)

# Sample job data
jobs_data = [
    {"title": "Delivery Assistant", "location": (26.7271, 88.3953), "pay": "₹500/day"},
    {"title": "Event Helper", "location": (26.6997, 88.3113), "pay": "₹700/day"}
]

# Sample worker data
workers_data = [
    {"name": "Ravi", "skill": "Delivery Helper", "experience": "2 years", "location": (26.5671, 88.3923)},
    {"name": "Anita", "skill": "Data Entry", "experience": "1 year", "location": (26.7001, 88.2953)},
    {"name": "Karan", "skill": "Event Setup", "experience": "3 years", "location": (26.3430, 88.3553)}
]

# Utility: convert Python tuples -> JS arrays
def normalize_data(data):
    normalized = []
    for item in data:
        new_item = item.copy()
        if "location" in new_item and isinstance(new_item["location"], tuple):
            new_item["location"] = list(new_item["location"])
        normalized.append(new_item)
    return normalized

@app.route("/")
def home():
    return render_template("index.html")

# Jobs
@app.route("/jobs", methods=["GET", "POST"])
def jobs():
    if request.method == "POST":
        title = request.form.get("title")
        location = request.form.get("location")
        pay = request.form.get("pay")
        if title and location and pay:
            jobs_data.append({"title": title, "location": location, "pay": pay})
        return redirect(url_for("jobs"))
    return render_template("jobs.html", jobs=jobs_data)

@app.route("/delete_job/<int:index>")
def delete_job(index):
    if 0 <= index < len(jobs_data):
        jobs_data.pop(index)
    return redirect(url_for("jobs"))

# Workers
@app.route("/workers", methods=["GET", "POST"])
def workers():
    if request.method == "POST":
        name = request.form.get("name")
        skill = request.form.get("skill")
        experience = request.form.get("experience")
        if name and skill and experience:
            workers_data.append({"name": name, "skill": skill, "experience": experience})
        return redirect(url_for("workers"))
    return render_template("workers.html", workers=workers_data)

@app.route("/delete_worker/<int:index>")
def delete_worker(index):
    if 0 <= index < len(workers_data):
        workers_data.pop(index)
    return redirect(url_for("workers"))

# Map
@app.route("/map")
def map_view():
    return render_template(
        "map.html",
        jobs=normalize_data(jobs_data),
        workers=normalize_data(workers_data)
    )

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5001))  # use PORT if available, else default 5000
    app.run(host="0.0.0.0", port=port, debug=True)

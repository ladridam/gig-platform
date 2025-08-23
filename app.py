from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Sample job data
jobs_data = [
    {"title": "Delivery Assistant", "location": "Siliguri", "pay": "₹500/day"},
    {"title": "Event Helper", "location": "Matigara", "pay": "₹700/day"}
]

# Sample worker data
workers_data = [
    {"name": "Ravi", "skill": "Delivery Helper", "experience": "2 years"},
    {"name": "Anita", "skill": "Data Entry", "experience": "1 year"},
    {"name": "Karan", "skill": "Event Setup", "experience": "3 years"}
]

@app.route("/")
def home():
    return render_template("index.html")

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

if __name__ == "__main__":
    app.run(debug=True)

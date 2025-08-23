from flask import Flask, render_template

app = Flask(__name__)

# Homepage
@app.route("/")
def home():
    return render_template("index.html")

# Jobs Page (dynamic data)
@app.route("/jobs")
def jobs():
    job_list = [
        {"title": "Delivery Helper", "duration": "5 hrs", "pay": "₹500"},
        {"title": "Data Entry", "duration": "2 hrs", "pay": "₹300"},
        {"title": "Event Setup Assistant", "duration": "1 day", "pay": "₹800"}
    ]
    return render_template("jobs.html", jobs=job_list)

# Workers Page
@app.route("/workers")
def workers():
    worker_list = [
        {"name": "Ravi", "skill": "Delivery Helper", "exp": "2 yrs"},
        {"name": "Anita", "skill": "Data Entry", "exp": "1 yr"},
        {"name": "Karan", "skill": "Event Setup", "exp": "3 yrs"}
    ]
    return render_template("workers.html", workers=worker_list)

if __name__ == "__main__":
    app.run(debug=True)

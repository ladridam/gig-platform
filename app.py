from flask import Flask, render_template
from geopy.distance import geodesic

app = Flask(__name__)
#Sample data
workers = [
    {"name": "Alice", "skills": ["plumbing", "carpentry"], "location": (40.7128, -74.0060)},  # New York
    {"name": "Bob", "skills": ["electrical", "plumbing"], "location": (40.7522, -74.2437)},
    {"name": "Charlie", "skills": ["carpentry", "painting"], "location": (40.8781, -74.6298)}
]
gigs = [
    {"title": "Fix my sink", "required_skill": "plumbing", "location": (40.730610, -73.935242)},  # New York
    {"title": "Paint my house", "required_skill": "painting", "location": (34.0422, -74.2539)},
    {"title": "Build a deck", "required_skill": "carpentry", "location": (40.8481, -74.6228)}
]
#routes
@app.route('/')
def home():
    return render_template('index.html', workers=workers, gigs=gigs)

@app.route('/match')
def match():
    results = []
    for gig in gigs:
        matched_workers = []
        for w in workers:
            # skill check + distance within 35 km
            if gig["skill"] in w["skills"]:
                dist = geodesic(gig["location"], w["location"]).km
                if dist <= 35:
                    matched_workers.append({"name": w["name"], "distance": round(dist,2)})
        results.append({"gig": gig["title"], "workers": matched_workers})
    return render_template("gigs.html", results=results)
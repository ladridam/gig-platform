from typing import Dict, Any
from gig_platform.extensions import db


class Job(db.Model):
    """Job model representing available gigs."""
    
    __tablename__ = "jobs"
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)
    pay = db.Column(db.String(50), nullable=False)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert job to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "title": self.title,
            "location": [self.lat, self.lng],
            "pay": self.pay,
        }
    
    def __repr__(self) -> str:
        return f"<Job {self.title}>"
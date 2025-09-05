from typing import Dict, Any
from gig_platform.extensions import db


class Worker(db.Model):
    """Worker model representing available workers."""
    
    __tablename__ = "workers"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    skill = db.Column(db.String(100), nullable=False)
    experience = db.Column(db.String(50), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert worker to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "skill": self.skill,
            "experience": self.experience,
            "location": [self.lat, self.lng],
        }
    
    def __repr__(self) -> str:
        return f"<Worker {self.name}>"
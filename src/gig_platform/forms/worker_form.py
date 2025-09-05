from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class WorkerForm(FlaskForm):
    """Form for creating and updating workers."""
    
    name = StringField(
        "Name", 
        validators=[DataRequired(), Length(min=2, max=100)]
    )
    skill = StringField(
        "Skill", 
        validators=[DataRequired(), Length(min=2, max=100)]
    )
    experience = StringField(
        "Experience", 
        validators=[DataRequired(), Length(min=2, max=50)]
    )
    location = StringField(
        "Location", 
        validators=[DataRequired(), Length(min=3, max=200)]
    )
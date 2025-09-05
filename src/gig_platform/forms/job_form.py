from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class JobForm(FlaskForm):
    """Form for creating and updating jobs."""
    
    title = StringField(
        "Job Title", 
        validators=[DataRequired(), Length(min=2, max=100)]
    )
    location = StringField(
        "Location", 
        validators=[DataRequired(), Length(min=3, max=200)]
    )
    pay = StringField(
        "Pay", 
        validators=[DataRequired(), Length(min=2, max=50)]
    )
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class MovieForm(FlaskForm):
    movie_name = StringField('Enter Movie Name...', validators=[DataRequired()])
    submit = SubmitField(label='Search')
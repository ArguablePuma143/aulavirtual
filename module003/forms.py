from flask_wtf import FlaskForm
from wtforms import SubmitField, TextField, TextAreaField, DateField
import datetime
from wtforms.validators import Required

class PostForm(FlaskForm):
    name = TextField("Name of the activity", validators=[Required()])
    description = TextAreaField("Description of the activity")
    deadline = DateField("Fecha límite de entrega", format="%d-%m-%Y %H:%M", default=datetime.datetime.today)
    submit = SubmitField('Submit')


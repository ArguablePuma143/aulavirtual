from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import Required

class PostForm(FlaskForm):
    body = TextAreaField("What's on your mind?", validators=[Required()])
    submit = SubmitField('Submit')


from flask_wtf import FlaskForm
from wtforms import SubmitField, TextField, TextAreaField, DateField
import datetime
from wtforms import validators
from wtforms.fields.core import FloatField, IntegerField
from wtforms.validators import Required, NumberRange
from flask_wtf.file import FileRequired, FileField, FileAllowed

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx'}
def allowed_file(filename):
    """
    @params: filename - name to be filtered
    @returns: A boolean depicting if it is allowed (True) or not (False)
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class PostForm(FlaskForm):
    name = TextField("Nombre de la actividad", validators=[Required()])
    description = TextAreaField("Descripción de la actividad")
    deadline = DateField("Fecha límite de entrega", format="%d-%m-%Y %H:%M", default=datetime.datetime.today)
    submit = SubmitField('Enviar')

class ActivityUploadForm(FlaskForm):
    file = FileField("PSube tu archivo",
                    validators= [FileRequired(), FileAllowed(ALLOWED_EXTENSIONS, "No se permite esa extensión")],
                    description="Entrega tu archivo")
    submit = SubmitField("Entregar")

class GradeForm(FlaskForm):
    grade = FloatField("Pon la nota aquí", validators=[NumberRange(min=0, max=10, message='Invalid length')])
    submit = SubmitField("Enviar")
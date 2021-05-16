from flask_wtf import FlaskForm
from wtforms import SubmitField, TextField, TextAreaField, DateField
import datetime
from wtforms.validators import Required
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
    name = TextField("Name of the activity", validators=[Required()])
    description = TextAreaField("Description of the activity")
    deadline = DateField("Fecha límite de entrega", format="%d-%m-%Y %H:%M", default=datetime.datetime.today)
    submit = SubmitField('Submit')

class ActivityUploadForm(FlaskForm):
    file = FileField("Put your file here", 
                    validators= [FileRequired(), FileAllowed(ALLOWED_EXTENSIONS, "No se permite esa extensión")], 
                    description="Entrega tu archivo")
    submit = SubmitField("Entregar")
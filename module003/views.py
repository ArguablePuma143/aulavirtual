from flask import Blueprint, render_template, flash, redirect, url_for
from flask.globals import request
from flask_login import login_required, current_user
from models import get_app, get_db, Follow, Course, Activity, ActivityUpload
from module003.forms import *
import os
from werkzeug.utils import secure_filename

from flask import send_from_directory

module003 = Blueprint("module003", __name__,static_folder="static",template_folder="templates")
db = get_db()
app = get_app()

UPLOAD_FOLDER = 'C:\\Users\\Javi\\Desktop\\Web Servidor\\proyecto\\aulavirtual\\module003\\subidas'


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@module003.route('/', methods=['GET', 'POST'])
def module003_index():
    courses = None
    coursesCreated = Course.query.filter(Course.user_id == current_user.id).all()
    coursesFollowed = Follow.query.filter(Follow.user_id == current_user.id).all()
    return render_template('module003_index.html',
                coursesFollowed=coursesFollowed,
                coursesCreated=coursesCreated,
                module="module003")

@module003.route('/<coursecode>', methods=['GET', 'POST'])
def module003_course(coursecode):
    form = PostForm()
    if form.validate_on_submit():
        activity = Activity(name=form.name.data,
        description=form.description.data,
        user_id = current_user.id,
        course_code = coursecode,
        dead_line = form.deadline.data)
        db.session.add(activity)
        db.session.commit()
        return redirect('/assignment/' + coursecode)
    coursesCreated = Course.query.filter(Course.user_id == current_user.id).all()
    coursesFollowed = Follow.query.filter(Follow.user_id == current_user.id).all()

    activities = Activity.query.filter(Activity.course_code == coursecode).all()

    creator_id = Course.query.filter(Course.code == coursecode).first().user_id
    return render_template('module003_activities.html',
         coursesFollowed=coursesFollowed,
         coursesCreated=coursesCreated,
         form=form, creator_id=creator_id,
         activities=activities,
         course_code=coursecode,
         module="module003"
        )

@module003.route('/<coursecode>/<activity_id>', methods=['GET', 'POST'])
def module003_activity(coursecode, activity_id):
    form = ActivityUploadForm()
    if form.validate_on_submit():
        try:
            file = request.files['file']

            filename = secure_filename(file.filename)
            folder = UPLOAD_FOLDER + "\\{user_id}\\{course_code}\\{activity_id}".format(
                user_id=current_user.id,
                course_code=coursecode,
                activity_id=activity_id)

            if not os.path.exists(folder):
                os.makedirs(folder, exist_ok=True)
            file.save(os.path.join(folder, filename))

            upload = ActivityUpload(
                user_id=current_user.id,
                activity_id = activity_id,
                content_link = filename)

            db.session.add(upload)
            db.session.commit()
        except os.error as e:
            flash("There was an error uploading your file, sorry")
            redirect("/")

    activity = Activity.query.get(activity_id)
    coursesCreated = Course.query.filter(Course.user_id == current_user.id).all()
    coursesFollowed = Follow.query.filter(Follow.user_id == current_user.id).all()

    return render_template("module003_activity.html", 
                            activity=activity,
                            coursesFollowed=coursesFollowed,
                            coursesCreated=coursesCreated,
                            form=form,
                            module="module003")

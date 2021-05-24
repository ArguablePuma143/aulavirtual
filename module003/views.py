from flask import Blueprint, render_template, flash, redirect, url_for
from flask.globals import request
from flask.helpers import send_file
from flask_login import login_required, current_user
from models import get_app, get_db, User, Follow, Course, Activity, ActivityUpload
from module003.forms import *

import ntpath
import os
from werkzeug.utils import secure_filename

from flask import send_from_directory

module003 = Blueprint("module003", __name__,static_folder="static",template_folder="templates")
db = get_db()
app = get_app()

UPLOAD_FOLDER = 'module003/subidas'


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@module003.route('/', methods=['GET', 'POST'])
@login_required
def module003_index():
    courses = None
    coursesCreated = Course.query.filter(Course.user_id == current_user.id).all()
    coursesFollowed = Follow.query.filter(Follow.user_id == current_user.id).all()

    codes = [ course.course_code for course in coursesFollowed]
    current_user_completed_activities = [ upload.activity_id for upload in ActivityUpload.query.filter(ActivityUpload.user_id == current_user.id)]
    print(current_user_completed_activities)
    
    activities = Activity.query.filter( Activity.course_code.in_(codes)).all()


    return render_template('module003_index.html',
                coursesFollowed=coursesFollowed,
                coursesCreated=coursesCreated,
                activities=activities,
                current_user_completed_activities=current_user_completed_activities,
                module="module003")

@module003.route('/<coursecode>', methods=['GET', 'POST'])
@login_required
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

    course = Course.query.filter( Course.code == coursecode).first()
    coursename = course.name
    creator_id = Course.query.filter(Course.code == coursecode).first().user_id
    return render_template('module003_activities.html',
         coursesFollowed=coursesFollowed,
         coursesCreated=coursesCreated,
         form=form,
         creator_id=creator_id,
         activities=activities,
         course_code=coursecode,
         course_name = coursename,
         module="module003"
        )

@module003.route('/<coursecode>/<activity_id>', methods=['GET', 'POST'])
@login_required
def module003_activity(coursecode, activity_id):
    form = ActivityUploadForm()
    if request.method == "POST" and form.validate_on_submit():
        try:
            file = request.files['file']

            filename = secure_filename(file.filename)
            folder = app.config["UPLOAD_FOLDER"] + "/{user_id}/{course_code}/{activity_id}".format(
                user_id=current_user.id,
                course_code=coursecode,
                activity_id=activity_id)

            if not os.path.exists(folder):
                os.makedirs(folder, exist_ok=True)
            file.save(os.path.join(folder, filename))

            upload = ActivityUpload(
                user_id=current_user.id,
                activity_id = activity_id,
                content_link = "{user_id}/{course_code}/{activity_id}/{filename}".format(
                    user_id=current_user.id,
                    course_code=coursecode,
                    activity_id=activity_id,
                    filename=filename))

            db.session.add(upload)
            db.session.commit()
        except os.error as e:
            flash("No se ha podido subir por un error en el servidor.")
            redirect("/")

        flash("Se ha subido la actividad con éxito")


    activity = Activity.query.get(activity_id)
    uploads = None
    student_uploads = None
    if current_user.id == activity.user_id:
        uploads = db.session.query(ActivityUpload.id, User.username, ActivityUpload.user_id, ActivityUpload.date_uploaded, ActivityUpload.grade, ActivityUpload.content_link)\
            .filter(ActivityUpload.activity_id == activity_id)\
            .join(User, User.id == ActivityUpload.user_id).all()
    else:
        student_uploads = ActivityUpload.query.filter(
            ActivityUpload.user_id == current_user.id,
            ActivityUpload.activity_id == activity_id
            )

    coursesCreated = Course.query.filter(Course.user_id == current_user.id).all()
    coursesFollowed = Follow.query.filter(Follow.user_id == current_user.id).all()

    return render_template("module003_activity.html",
                            activity=activity,
                            coursesFollowed=coursesFollowed,
                            coursesCreated=coursesCreated,
                            form=form,
                            uploads=uploads,
                            is_professor = True if current_user.id == activity.user_id else False,
                            student_uploads=student_uploads,
                            module="module003")

@module003.route('/download/<upload_id>')
@login_required
def download(upload_id):
    upload = ActivityUpload.query.get(upload_id)

    path = upload.content_link.replace("\\", "/")

    return send_from_directory(app.config["UPLOAD_FOLDER"], path, as_attachment=True)

@module003.route('/grade/<upload_id>', methods=["GET", "POST"])
@login_required
def grade(upload_id):
    upload = db.session.query(ActivityUpload.id, User.username, ActivityUpload.user_id, ActivityUpload.date_uploaded, ActivityUpload.grade, ActivityUpload.content_link, ActivityUpload.activity_id)\
                    .filter(ActivityUpload.id == upload_id)\
                    .join(User, User.id == ActivityUpload.user_id).first()
    form = GradeForm(grade=upload.grade)
    if request.method == "POST" and form.validate_on_submit():
        targetUpload = ActivityUpload.query.get(upload_id)
        targetUpload.grade = form.grade.data

        db.session.commit()

    coursesCreated = Course.query.filter(Course.user_id == current_user.id).all()
    coursesFollowed = Follow.query.filter(Follow.user_id == current_user.id).all()

    activity = Activity.query.get(upload.activity_id)

    return render_template("module003_grade.html",
                            upload=upload,
                            coursesCreated=coursesCreated,
                            coursesFollowed=coursesFollowed,
                            form=form,
                            is_creator= current_user.id == activity.user_id,
                            module="module003")
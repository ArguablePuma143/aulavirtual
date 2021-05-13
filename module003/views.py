from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from models import get_db, Follow, Course, Activity
from module003.forms import *

module003 = Blueprint("module003", __name__,static_folder="static",template_folder="templates")
db = get_db()

@module003.route('/', methods=['GET', 'POST'])
def module003_index():
    courses = None
    coursesCreated = Course.query.filter(Course.user_id == current_user.id).all()
    coursesFollowed = Follow.query.filter(Follow.user_id == current_user.id).all()
    return render_template('module003_index.html', coursesFollowed=coursesFollowed, coursesCreated=coursesCreated)

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
         course_code=coursecode
        )

@module003.route('/<coursecode>/<activity_id>', methods=['GET', 'POST'])
def module003_activity(coursecode, activity_id):
    activity = Activity.query.get(activity_id)
    return render_template("module003_activity.html", activity=activity)

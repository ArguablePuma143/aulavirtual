from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from models import get_db, Post, Course, Follow
from module002.forms import *

db = get_db()
module002 = Blueprint("module002", __name__,static_folder="static",template_folder="templates")

@module002.route('/test')
def module002_test():
    return 'OK'

@module002.route('/', methods=['GET', 'POST'])
def module002_index():
    courses = Follow.query.filter(Follow.user_id == current_user.id).all()
    return render_template('module002_index.html', courses=courses, module="module002")

@module002.route('/<coursecode>', methods=['GET', 'POST'])
def module002_course(coursecode):
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.body.data,
        author=current_user._get_current_object(),
        course_code=coursecode)
        db.session.add(post)
        db.session.commit()
        return redirect('/board/' + coursecode)
    posts = Post.query.filter(Post.course_code==coursecode).order_by(Post.timestamp.desc()).all()
    courses = Follow.query.filter(Follow.user_id == current_user.id).all()
    actualCourse = Follow.query.filter(Follow.course_code == coursecode).first()
    return render_template('module002_course.html', form=form, posts=posts, courses=courses, module="module002", actualCourse=actualCourse)


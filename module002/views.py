from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from models import get_db, Post
from module002.forms import *

db = get_db()
module002 = Blueprint("module002", __name__,static_folder="static",template_folder="templates")

@module002.route('/test')
def module002_test():
    return 'OK'

@module002.route('/', methods=['GET', 'POST'])
def module002_index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.body.data,
        author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('module002.module002_index'))
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('module002_index.html', form=form, posts=posts)


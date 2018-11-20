from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from pro_files.auth import login_required
from pro_files.db import get_db

bp = Blueprint('student', __name__)


@bp.route('/s_home')
@login_required
def home():
    db = get_db()
    projects = db.execute(
        'select id, teacher_id, title, description, course_code, semester, progress from project where student_id = ?', (g.user['id'],)
    ).fetchall()
    return render_template('student/s_home.html', projects=projects)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        db = get_db()

        s_id = db.execute(
            'select id from student where id = ?', (g.user['id'],)
            ).fetchone()
        
        title = request.form['title']
        description = request.form['description']
        t = db.execute(
            'select * from teacher where email = ?', (request.form['email'],)
            ).fetchone()

        if t is None:
            error = 'Teacher is not registered'

        course_code = request.form['course_code']
        semester = request.form['semester']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db.execute(
                'insert into project (student_id, title, description, teacher_id, course_code, semester) values (?, ?, ?, ?, ?, ?)', 
                (g.user['id'], title, description, t['id'], course_code, semester)
            )
            db.commit()
            return redirect(url_for('student.home'))

    return render_template('student/create.html')
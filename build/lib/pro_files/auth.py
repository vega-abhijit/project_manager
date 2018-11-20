import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from pro_files.db import get_db


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/s_register', methods=('GET', 'POST'))
def s_register():
	if request.method == 'POST':
		name = request.form['name']
		reg_id = request.form['reg']
		email = request.form['email']
		session = request.form['session']
		dept = request.form['dept']
		password = request.form['password']
		confirm_password = request.form['confirm_password']

		db = get_db()
		error = None

		if not name:
			error = 'Full Name is required'
		elif not reg_id:
			error = 'Registration No. is required'
		elif not email:
			error = 'Email is Required'
		elif not session:
			error = 'Session is required'
		elif not dept:
			error = 'Department Code is required'
		elif not password:
			error = 'Password is required'
		elif not confirm_password:
			error = 'Confirm Password is required'
		elif db.execute(
			'select id from student where id = ?', (reg_id,)
			).fetchone() is not None:
			error = 'User is already registered'
		elif password != confirm_password:
			error = 'Password doesn\'t match'

		if error is None:
			db.execute(
				'insert into student (id, email, name, dept, session, password) values (?,?,?,?,?,?)', (reg_id, email, name, dept, session, generate_password_hash(password))
				)
			db.commit()
			return redirect(url_for('auth.s_login'))

		flash(error)

	
	return render_template('auth/s_register.html')


@bp.route('/t_register', methods=('GET', 'POST'))
def t_register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        dept = request.form['dept']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        #from . import db
        db = get_db()
        error = None

        if not name:
            error = 'Full Name is required'
        elif not email:
            error = 'Email is required'
        elif not dept:
            error = 'Department Code is required'
        elif not password:
            error = 'Password is required'
        elif not confirm_password:
            error = 'Confirm Password is required'
        elif db.execute(
            'select email from teacher where email = ?', (email,)
            ).fetchone() is not None:
            error = 'User is already registered.'
        elif password != confirm_password:
            error = 'Password doesn\'t match'

        if error is None:
            db.execute(
                'insert into teacher (email, name, dept, password) values (?,?,?,?)', (email, name, dept, generate_password_hash(password))
                )
            db.commit()
            return redirect(url_for('auth.t_login'))

        flash(error)

    return render_template('auth/t_register.html')


@bp.route('/s_login', methods=('GET', 'POST'))
def s_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'select * from student WHERE email = ?', (email,)
        	).fetchone()

        if user is None:
        	error = 'Incorrect username'
        elif not check_password_hash(user['password'], password):
        	error = 'Incorrect Password'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('student.home'))

        flash(error)

    return render_template('auth/s_login.html')

@bp.route('/t_login', methods=('GET', 'POST'))
def t_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'select * from teacher WHERE email = ?', (email,)
        	).fetchone()

        if user is None:
        	error = 'Incorrect username'
        elif not check_password_hash(user['password'], password):
        	error = 'Incorrect Password'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('teacher.home'))

        flash(error)

    return render_template('auth/t_login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    db = get_db()

    if user_id is None:
        g.user = None
    else:
        g.user = db.execute(
            'select * from student where id = ?', (user_id,)
        ).fetchone()

        if g.user is None:
        	g.user = db.execute(
        		'select * from teacher where id = ?', (user_id,)
        	).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('root'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.s_login'))

        return view(**kwargs)

    return wrapped_view	
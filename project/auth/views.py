from flask import render_template, Blueprint, flash, request, session, \
    redirect, url_for
from .forms import LoginForm, RegisterForm
from .decorators import login_required
from project.models import User

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form = LoginForm(request.form)
        if form.validate_on_submit():
            user = User.authenticate(**form.data)
            if user:
                session['user_id'] = user.id
                return redirect(url_for('admin.vacancy_list'))
            else:
                flash("Неправильный логин и/или пароль")
    else:
        if session.get('user_id'):
            return redirect(url_for('admin.vacancy_list'))
        form = LoginForm()
    return render_template('login.html',
                           title='Sign in',
                           form=form)


@auth.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    if request.method == 'POST':
        form = RegisterForm(request.form)
        if form.validate_on_submit():
            userdata = form.data
            userdata.pop('confirmation')
            u = User(**userdata)
            u.save()
            flash("Вы успешно зарегистрировались")
            return redirect(url_for('auth.login'))
    else:
        form = RegisterForm()
    return render_template('login.html',
                           title='Registration',
                           form=form)


@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    session.pop('user_id', None)
    return redirect(url_for('auth.login'))

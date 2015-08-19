from flask import render_template, flash, session, redirect, \
    url_for, abort
from .forms import LoginForm, ResetForm, PasswordEditForm
from .decorators import login_required
from project.models import User
from project.blueprints import auth_app


@auth_app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.bl.authenticate(**form.data)
        if user:
            session['user_id'] = user.id
            session['user_login'] = user.login
            return redirect(url_for('admin.mainpage'))
        else:
            flash("Неправильный логин и/или пароль")

    if session.get('user_id'):
        return redirect(url_for('admin.mainpage'))

    return render_template(
        'login.html',
        title='Вход',
        submit='Войти',
        form=form,
    )


@auth_app.route('/reset', methods=['GET', 'POST'])
def reset():
    form = ResetForm()
    if form.validate_on_submit():
        User.bl.forgot_password(form.data['email'])
        flash("Вам на почту отправлено письмо с дальнейшими инструкциями")
        return redirect(url_for('auth.login'))
    return render_template(
        'login.html',
        title='Сброс пароля',
        submit='Сбросить',
        form=form,
    )


@auth_app.route('/reset/<token>', methods=['GET', 'POST'])
def confirm_reset(token):
    success = User.bl.reset_password(token)
    if success:
        flash("Вы успешно сбросили пароль! "
              "Новый пароль отправлен по электронной почте")
        return redirect(url_for('auth.login'))
    else:
        abort(404)


@auth_app.route('/password_change', methods=['GET', 'POST'])
@login_required()
def change_password():
    form = PasswordEditForm()
    if form.validate_on_submit():
        User.bl.set_password(form.data['new_password'])
        flash('Ваш пароль успешно изменён')
        return redirect(url_for('admin.mainpage'))
    return render_template(
        'login.html',
        title='Смена пароля',
        submit='Сменить',
        form=form,
    )


@auth_app.route('/logout', methods=['GET'])
@login_required()
def logout():
    session.pop('user_id', None)
    session.pop('user_login', None)
    return redirect(url_for('auth.login'))

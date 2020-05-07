from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_user, logout_user, login_required
from database import session
from models.user import User
from models.role import Role
from forms.register import RegisterForm
from forms.login import LoginForm
from utils.passwords import simple_passwords

blueprint = Blueprint('auth', __name__, url_prefix='/auth')


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data in simple_passwords:
            return render_template('auth/register.html',
                                   title='Регистрация',
                                   form=form,
                                   message='Слишком простой пароль')
        if form.password.data != form.password_again.data:
            return render_template('auth/register.html',
                                   title='Регистрация',
                                   form=form,
                                   message='Пароли не совпадают')
        connect = session.create_session()
        if connect.query(User).filter(User.email == form.email.data).first():
            return render_template('auth/register.html',
                                   title='Регистрация',
                                   form=form,
                                   message='Такой пользователь уже есть')
        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        role = connect.query(Role).filter(Role.slug == 'user').first()
        role.users.append(user)
        connect.merge(role)
        connect.commit()
        return redirect(url_for('.login'))
    return render_template('auth/register.html', title='Регистрация', form=form)


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        connect = session.create_session()
        user = connect.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('main.index'))
        return render_template('auth/login.html',
                               message='Неправильный логин или пароль',
                               form=form)
    return render_template('auth/login.html', title='Авторизация', form=form)


@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

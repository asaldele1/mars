from flask import Blueprint, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from data import db_session
from data.users import User
from forms.login import LoginForm
from forms.register import RegisterForm


bp = Blueprint('auth', __name__)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(
            User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template('login.html', title='Авторизация', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@bp.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            form.email.errors.append('Email уже зарегистрирован')
            return render_template('register.html', title='Регистрация', form=form)
        user = User(
            email=form.email.data,
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect(url_for('auth.login'))
    return render_template('register.html', title='Регистрация', form=form)

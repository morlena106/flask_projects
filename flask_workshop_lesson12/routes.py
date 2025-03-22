import email
from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import Email, EqualTo, InputRequired, Length

from db.database import session_scope
from db.models import User
from werkzeug.security import generate_password_hash, check_password_hash

main_blueprint = Blueprint("main", __name__)


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField(
        "Password", validators=[InputRequired(), Length(min=8, max=36)]
    )


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[InputRequired(), Length(max=100, min=4)]
    )
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField(
        "Password", validators=[InputRequired(), Length(min=8, max=36)]
    )
    confirm_password = PasswordField(
        "Confirm Password", validators=[InputRequired(), EqualTo("password")]
    )


@main_blueprint.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        with session_scope() as session:
            user = session.query(User).filter_by(email=form.email.data).first()
        if user:
            flash("User with this email already exists!", 'danger')
            return redirect(url_for("main.register", form=form),)

        user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data),
        )
        with session_scope() as session:
            session.add(user)
        return redirect(url_for("main.login"))
    elif form.errors:
        flash(form.errors, category='danger')

    return render_template("register.html", form=form)


@main_blueprint.route("/main")
@login_required
def main_route():
    return render_template("home.html", name=current_user.username)

@main_blueprint.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        with session_scope() as session:
            user = session.query(User).filter_by(email=form.email.data).first()
            if user and check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                return redirect(url_for('main.main_route'))
        flash('Login failed', 'danger')
    return render_template('login.html', form=form)


@main_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.login'))

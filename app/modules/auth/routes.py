from flask import render_template, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from flask_dance.contrib.github import make_github_blueprint, github
from app.modules.auth import auth_bp
from app.modules.auth.forms import SignupForm, LoginForm
from app.modules.auth.services import AuthenticationService
from app.modules.profile.services import UserProfileService
import os

# Servicios
authentication_service = AuthenticationService()
user_profile_service = UserProfileService()

# Configuración del Blueprint de GitHub
github_blueprint = make_github_blueprint(
    client_id=os.getenv("GITHUB_CLIENT_ID"),
    client_secret=os.getenv("GITHUB_CLIENT_SECRET"),
    redirect_to="auth.github_callback"
)

auth_bp.register_blueprint(github_blueprint, url_prefix="/auth/github")


@auth_bp.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))

    form = SignupForm()
    if form.validate_on_submit():
        email = form.email.data
        if not authentication_service.is_email_available(email):
            return render_template("auth/signup_form.html", form=form, error=f'Email {email} in use')

        try:
            user = authentication_service.create_with_profile(**form.data)
        except Exception as exc:
            return render_template("auth/signup_form.html", form=form, error=f'Error creating user: {exc}')

        login_user(user, remember=True)
        return redirect(url_for('public.index'))

    return render_template("auth/signup_form.html", form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))

    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        if authentication_service.login(form.email.data, form.password.data):
            return redirect(url_for('public.index'))

        return render_template("auth/login_form.html", form=form, error='Invalid credentials')

    return render_template('auth/login_form.html', form=form)


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('public.index'))


@auth_bp.route('/auth/github/login')
def github_login():

    if not github.authorized:
        return redirect(url_for("github.login"))

    resp = github.get("/user")
    if not resp.ok:
        return redirect(url_for("auth.login"))

    github_info = resp.json()
    github_id = github_info.get("id")
    email = github_info.get("email")
    name = github_info.get("login")
    surname = github_info.get("name")

    user = authentication_service.get_or_create_user_from_github(github_id, email, name, surname)
    login_user(user)
    return redirect(url_for("public.index"))


# Callback de GitHub, se ejecuta al regresar desde GitHub tras la autorización
@auth_bp.route("/auth/github/authorized")
def github_callback():
    if not github.authorized:
        return redirect(url_for("github.login"))  # Vuelve a pedir autorización si no se ha completado

    resp = github.get("/user")
    if not resp.ok:
        return redirect(url_for("auth.login"))

    github_info = resp.json()
    github_id = github_info.get("id")
    email = github_info.get("email")
    name = github_info.get("login")
    surname = github_info.get("name")

    print(github_info)

    user = authentication_service.get_or_create_user_from_github(github_id, email, name, surname)
    login_user(user)  # Inicia sesión con el usuario creado

    return redirect(url_for("public.index"))

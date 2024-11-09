import os
from flask import render_template, redirect, url_for, request, session, flash, current_app as app
from flask import render_template, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport import requests


from app.modules.auth import auth_bp
from app.modules.auth.forms import SignupForm, LoginForm, ForgotPasswordForm
from app.modules.auth.services import AuthenticationService
from app.modules.profile.services import UserProfileService
from app.modules.auth.email_service import EmailService, generate_otp

authentication_service = AuthenticationService()
user_profile_service = UserProfileService()

CLIENT_SECRETS_FILE = os.getenv("GOOGLE_CLIENT_SECRETS_FILE")
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
email = os.getenv('EMAIL')
password = os.getenv('EMAIL_PASS')
code = generate_otp()

authentication_service = AuthenticationService()
user_profile_service = UserProfileService()
email_service = EmailService(email,password, code)

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
            #Para enviar email, es provisional y no deberia ir aquí pero era para probar backend
            email_service.connecting_sender(email)
        except Exception as exc:
            app.logger.error(f"Error creating user: {exc}")
            return render_template("auth/signup_form.html", form=form, error=f'Error creating user: {exc}')

        login_user(user, remember=True)
        app.logger.info(f"User created and logged in: {user.email}")
        return redirect(url_for('public.index'))

    return render_template("auth/signup_form.html", form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))

    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        if authentication_service.login(form.email.data, form.password.data):
            app.logger.info(f"User logged in: {form.email.data}")
            return redirect(url_for('public.index'))

        app.logger.warning(f"Login failed for email: {form.email.data}")
        return render_template("auth/login_form.html", form=form, error='Invalid credentials')
    
    return render_template('auth/login_form.html', form=form)

@auth_bp.route("/forgotpassword/", methods=["GET", "POST"])
def show_forgotpassword_form():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))

    form = ForgotPasswordForm()
    if form.validate_on_submit():
        email = form.email.data
        if authentication_service.is_email_available(email):
            return render_template("auth/forgotpassword_form.html", form=form, error=f'The email address {email} is not registered.')
        else:
            email_service.connecting_sender(email)
        return redirect(url_for('public.index'))
    return render_template("auth/forgotpassword_form.html", form=form)

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('public.index'))

SCOPES = [
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/userinfo.email",
    "openid"
]

@auth_bp.route('/login/google')
def google_login():
    session.permanent = True
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    authorization_url, state = flow.authorization_url(prompt='consent')
    session['state'] = state
    return redirect(authorization_url)

@auth_bp.route('/auth/google/callback')
def google_callback():
    app.logger.info(f"Recibiendo respuesta de Google: {request.args}")
    
    if 'state' not in session or request.args.get('state') != session['state']:
        flash("State value does not match. Possible CSRF attack.", "error")
        return redirect(url_for("auth.login"))

    
    session.pop('state', None)

    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )

    try:
        flow.fetch_token(authorization_response=request.url)
        app.logger.info("Token de Google obtenido correctamente.")
    except Exception as e:
        flash(f"Error al obtener el token de Google: {e}", "error")
        return redirect(url_for("auth.login"))

    credentials = flow.credentials
    token = credentials.id_token
    app.logger.info(f"ID Token recibido: {token}")
    
    try:
        id_info = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
    except ValueError as e:
        flash(f"Error de verificación de token: {e}", "error")
        return redirect(url_for("auth.login"))

    try:
        existing_user = authentication_service.get_user_by_email(id_info['email'])
        if existing_user:
            login_user(existing_user)
        else:
            user = authentication_service.get_or_create_user(id_info)
            login_user(user)
    except Exception as exc:
        flash(f"Error durante la creación del usuario: {exc}", "error")

    return redirect(url_for('public.index'))

import os
from flask import render_template, redirect, url_for, request, session, flash
from flask_login import current_user, login_user, logout_user
from flask_dance.contrib.github import make_github_blueprint, github
from app.modules.auth import auth_bp
from app.modules.auth.forms import SignupForm, LoginForm, ForgotPasswordForm, CodeForm, ResetPasswordForm, SignupCodeForm
from app.modules.auth.services import AuthenticationService
from app.modules.profile.services import UserProfileService

# Servicios
from app.modules.auth.services import EmailService


email = os.getenv('EMAIL')
password = os.getenv('EMAIL_PASS')

authentication_service = AuthenticationService()
user_profile_service = UserProfileService()
email_service = EmailService(email, password)

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
    code_validation_form = SignupCodeForm()
    if form.validate_on_submit():
        session['temp_user_data'] = form.data

        email = form.email.data
        if not authentication_service.is_email_available(email):
            return render_template("auth/signup_form.html", form=form, error=f'Email {email} in use')
        try:
            code = authentication_service.generate_signup_verification_token(email)
            msg = "Your verification code is: " + code + ". Please enter this code to complete the registration."
            email_service.send_mail(email, msg, "Verification Code")
            return render_template("auth/signup_code_validation_form.html", form=code_validation_form)
        except Exception as exc:
            return render_template("auth/signup_form.html", form=form, error=f'Could not send email to {email}')
    return render_template("auth/signup_form.html", form=form)


@auth_bp.route("/signup/code-validation", methods=["GET", "POST"])
def validate_code():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))

    code_validation_form = SignupCodeForm()
    if code_validation_form.validate_on_submit():
        try:
            temp_user_data = session.get('temp_user_data', None)
            if not temp_user_data:
                return render_template("auth/signup_code_validation_form.html",
                                       form=code_validation_form, error='Invalid session data: did not find temp_user_data')
            submitted_code = code_validation_form.code.data
            email = temp_user_data.get('email')
            if not email:
                return render_template("auth/signup_code_validation_form.html",
                                       form=code_validation_form, error='Invalid session data: email not found')
            if not authentication_service.validate_signup_verification_token(email, submitted_code):
                return render_template("auth/signup_code_validation_form.html",
                                       form=code_validation_form, error='Invalid code')
            
            user = authentication_service.create_with_profile(**temp_user_data)

        except Exception as exc:
            return render_template("auth/signup_code_validation_form.html",
                                   form=code_validation_form, error=f'Error creating user: {exc}')

        login_user(user, remember=True)
        return redirect(url_for('public.index'))

    return render_template("auth/signup_code_validation_form.html", form=code_validation_form)


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

  
@auth_bp.route("/forgotpassword/", methods=["GET", "POST"])
def show_forgotpassword_form():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))

    form = ForgotPasswordForm()
    formCode = CodeForm()
    if form.validate_on_submit():
        email = form.email.data
        if authentication_service.is_email_available(email):
            return render_template("auth/forgotpassword_form.html", form=form, error=f'The email address {email} is not registered.')
        try:
            otp_code = authentication_service.generate_resetpassword_verification_token(email)
            msg = f"Your OTP code is: {otp_code}. Please use this to reset your password."
            email_service.send_mail(email, msg, "Password Reset OTP")
            
            session['temp_user_data'] = {'email': email}
            
            return render_template("auth/validatecode_form.html", form=formCode)
        
        except Exception as exc:
            return render_template("auth/forgotpassword_form.html", form=form, error=f"Error sending OTP: {exc}")

    return render_template("auth/forgotpassword_form.html", form=form)

  
@auth_bp.route("/forgotpassword/code-validation", methods=["GET", "POST"])
def validate_forgotpassword_code():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))

    form = CodeForm()
    formPassword = ResetPasswordForm()
    if form.validate_on_submit():
        try:
            temp_user_data = session.get('temp_user_data', None)
            if not temp_user_data:
                return render_template("auth/validatecode_form.html", form=form, error="Invalid session data: did not find temp_user_data")

            email = temp_user_data.get('email')
            entered_code = form.code.data

            if not authentication_service.validate_resetpassword_verification_token(email, entered_code):
                return render_template("auth/validatecode_form.html", form=form, error="Invalid OTP code. Please try again.")
            
            return render_template("auth/resetpassword_form.html", form=formPassword)

        except Exception as exc:
            return render_template("auth/validatecode_form.html", form=form, error=f"Error validating OTP: {exc}")

    return render_template("auth/validatecode_form.html", form=form)

  
@auth_bp.route('/resetpassword/', methods=['GET', 'POST'])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))

    form = ResetPasswordForm()

    temp_user_data = session.get('temp_user_data', None)
    if not temp_user_data:
        return render_template("auth/resetpassword_form.html", form=form, error="Invalid session data: did not find temp_user_data")
    if form.validate_on_submit():
        new_password = form.password.data
        confirm_password = form.confirm_password.data

        if new_password != confirm_password:
            return render_template("auth/resetpassword_form.html", form=form, error="Passwords do not match.")
        try:
            email = temp_user_data.get('email')
            authentication_service.reset_password(email, new_password)

            session.pop('temp_user_data', None)
            return redirect(url_for('public.index'))

        except Exception as exc:
            return render_template("auth/resetpassword_form.html", form=form, error=f"Error resetting password: {exc}")

    return render_template("auth/resetpassword_form.html", form=form)

  
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

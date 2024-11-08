import os
from flask import render_template, redirect, url_for, request, session
from flask_login import current_user, login_user, logout_user


from app.modules.auth import auth_bp
from app.modules.auth.forms import SignupForm, LoginForm, ForgotPasswordForm, CodeForm, ResetPasswordForm
from app.modules.auth.services import AuthenticationService
from app.modules.profile.services import UserProfileService
from app.modules.auth.email_service import EmailService, generate_otp

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
            return render_template("auth/signup_form.html", form=form, error=f'Error creating user: {exc}')

        # Log user
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
            session['otp_code'] = code
            session['otp_email'] = email
            email_service.connecting_sender(email)
        return redirect(url_for('auth.validate_code'))
    return render_template("auth/forgotpassword_form.html", form=form)

@auth_bp.route("/validatecode/", methods=["GET", "POST"])
def validate_code():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))

    formCode = CodeForm()
    if formCode.validate_on_submit():
        entered_code = formCode.code.data
        stored_code = session.get('otp_code')
        if entered_code == stored_code:
            return redirect(url_for('auth.reset_password'))
        else:
            return render_template('auth/validatecode_form.html', form=formCode, error="Invalid code. Please try again.")
    return render_template('auth/validatecode_form.html', form=formCode)

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('public.index'))

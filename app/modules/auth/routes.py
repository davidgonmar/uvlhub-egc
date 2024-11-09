import os
from flask import render_template, redirect, url_for, request, session
from flask_login import current_user, login_user, logout_user

from app.modules.auth import auth_bp
from app.modules.auth.forms import SignupForm, LoginForm, ForgotPasswordForm, CodeForm, ResetPasswordForm, SignupCodeForm
from app.modules.auth.services import AuthenticationService
from app.modules.profile.services import UserProfileService
from app.modules.auth.email_service import EmailService


email = os.getenv('EMAIL')
password = os.getenv('EMAIL_PASS')

authentication_service = AuthenticationService()
user_profile_service = UserProfileService()
email_service = EmailService(email, password)


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
            email_service.connecting_sender(email, code)
            return render_template("auth/signup_code_validation_form.html", form=code_validation_form)
        except Exception as exc:
            print(exc)
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
    if form.validate_on_submit():
        email = form.email.data
        if authentication_service.is_email_available(email):
            return render_template("auth/forgotpassword_form.html", form=form, error=f'The email address {email} is not registered.')
        else:
            session['otp_code'] = code
            session['otp_email'] = email
            email_service.connecting_sender(email)
        return redirect(url_for('auth.validate_password_code'))
    return render_template("auth/forgotpassword_form.html", form=form)

  
@auth_bp.route("/validatecode/", methods=["GET", "POST"])
def validate_password_code():
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

  
@auth_bp.route('/resetpassword/', methods=['GET', 'POST'])
def reset_password():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        new_password = form.password.data
        confirm_password = form.confirm_password.data

        if new_password != confirm_password:
            return render_template("auth/resetpassword_form.html", form=form, error="Passwords do not match.")
        try:
            email = session.get('otp_email')
            authentication_service.reset_password(email, new_password)
            user = authentication_service.get_user_by_email(email)
            login_user(user, remember=True)
            return redirect(url_for('public.index'))
        except Exception as exc:
            return render_template("auth/resetpassword_form.html", form=form, error=f"Error resetting password: {exc}")

    return render_template("auth/resetpassword_form.html", form=form)

  
@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('public.index'))

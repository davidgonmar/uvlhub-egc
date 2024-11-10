import os
from flask import render_template, redirect, url_for, request, session, current_app
from flask_login import current_user, login_user, logout_user

from app.modules.auth import auth_bp
from app.modules.auth.forms import SignupForm, LoginForm, ForgotPasswordForm, CodeForm, ResetPasswordForm, SignupCodeForm
from app.modules.auth.services import AuthenticationService
from app.modules.profile.services import UserProfileService
from app.modules.auth.email_service import EmailService, generate_otp


from app.modules.auth.models import User
from app.modules.profile.models import UserProfile
from app import db


email = os.getenv('EMAIL')
password = os.getenv('EMAIL_PASS')
code = generate_otp()

authentication_service = AuthenticationService()
user_profile_service = UserProfileService()
email_service = EmailService(email, password, code)


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
            email_service.connecting_sender(email)
            return render_template("auth/signup_code_validation_form.html", form=code_validation_form)
        except Exception as exc:
            return render_template("auth/signup_form.html", form=form, error=f'Error creating user: {exc}')

    return render_template("auth/signup_form.html", form=form)


@auth_bp.route("/signup/code-validation", methods=["GET", "POST"])
def validate_code():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))

    code_validation_form = SignupCodeForm()
    if code_validation_form.validate_on_submit():
        try:
            temp_user_data = session.get('temp_user_data')
            session.pop('temp_user_data', None)
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

@auth_bp.before_app_request
def before_request():
    current_app.orcid_service = AuthenticationService()

@auth_bp.route('/orcid/login')
def login_orcid():
    redirect_uri = url_for('auth.authorize_orcid', _external=True, _scheme='http')
    return current_app.orcid_service.orcid_client.authorize_redirect(redirect_uri)

@auth_bp.route('/orcid/authorize')
def authorize_orcid():
    token = current_app.orcid_service.orcid_client.authorize_access_token()
    resp = current_app.orcid_service.orcid_client.get('https://orcid.org/oauth/userinfo', token=token)
    user_info = resp.json()

    orcid_id = user_info['sub']
    full_profile = current_app.orcid_service.get_orcid_full_profile(orcid_id, token)

    # Acceder a la afiliación
    affiliation_group = full_profile.get('activities-summary', {}).get('employments', {}).get('affiliation-group', [])
    if affiliation_group:
        employment_summary = affiliation_group[0].get('summaries', [{}])[0].get('employment-summary', {})
        organization = employment_summary.get('organization', {})
        affiliation = organization.get('name', '')
    else:
        affiliation = ''

    # Obtener información disponible del perfil público de ORCID
    given_name = user_info.get('given_name', '')
    family_name = user_info.get('family_name', '')
    surname = family_name if family_name else ""

    
    # Obtener el correo electrónico del perfil completo
    email = ''
    email_data = full_profile.get('person', {}).get('emails', {}).get('email', [])
    if email_data:
        email = email_data[0].get('email', '')

    # Verificar si el ORCID iD ya está registrado
    user_record = User.query.filter_by(orcid_id=orcid_id).first()
    
    if user_record:
        # Si el registro existe, obtener el perfil del usuario asociado
        profile = UserProfile.query.filter_by(id=user_record.id).first()
        if profile:
            user = User.query.get(profile.user_id)
            login_user(user)
            return redirect('/')
    else:
        # Crear usuario y perfil
        user = User()
        user.set_password(orcid_id)  # Usar el ORCID como contraseña
        user.email = email
        user.orcid_id=orcid_id
        db.session.add(user)
        db.session.commit()

        profile = UserProfile(
            user_id=user.id,
            name=given_name,
            surname=surname,
            affiliation=affiliation,
            orcid=orcid_id
        )
        db.session.add(profile)
        db.session.commit()
        db.session.commit()

        login_user(user)
        return redirect('/')

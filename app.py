import json
from flask import Flask, render_template, redirect, url_for, flash, session, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from forms import RegistrationForm, LoginForm, ScreeningForm, DemographicForm, SurveyForm, FieldHorticulturalCropsForm
from models import db, User, Survey, FieldHorticulturalCrops, Demographic
from decimal import Decimal
from flask_mail import Mail, Message
import secrets
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['MAIL_SERVER'] = 'smtp.your-email-provider.com'
app.config['MAIL_PORT'] = 587 
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'your-email@example.com'
app.config['MAIL_PASSWORD'] = 'your-email-password'
app.config['MAIL_DEFAULT_SENDER'] = 'your-email@example.com'

mail = Mail(app)

db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def generate_otp(length=6):
    """Generate a random OTP of given length."""
    digits = "0123456789"
    otp = ''.join(secrets.choice(digits) for _ in range(length))
    return otp

def send_otp_email(user_email, otp):
    """Send an OTP to the user's email address."""
    msg = Message('Your OTP for Verification', recipients=[user_email])
    msg.body = f'Your OTP is: {otp}\n\nThis OTP is valid for 10 minutes.'
    mail.send(msg)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/location', methods=['POST'])
@login_required
def update_location():
    data = request.json
    latitude = data.get('latitude')
    longitude = data.get('longitude')

    if not latitude or not longitude:
        return jsonify({'error': 'Invalid data'}), 400

    current_user.latitude = latitude
    current_user.longitude = longitude
    db.session.commit()

    return jsonify({'success': 'Location updated successfully'})

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        declaration = request.form.get('declaration')

        if declaration != 'agree':
            flash('You must agree to the declaration to register.', 'warning')
            return redirect(url_for('register'))

        if User.query.filter_by(email=form.email.data).first():
            flash('An account with this email already exists. Please use a different email.', 'danger')
            return redirect(url_for('register'))

        base_username = f"{form.first_name.data.lower()}{form.surname.data[0].lower()}"
        username = base_username

        # Generate a unique username if necessary
        counter = 1
        while User.query.filter_by(username=username).first():
            username = f"{base_username}{counter}"
            counter += 1

        user = User(
            username=username,
            first_name=form.first_name.data,
            surname=form.surname.data,
            email=form.email.data,
            phone_number=form.phone_number.data,
            address=form.address.data
        )
        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash(f'Account created for {form.first_name.data}!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('screening'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/send_otp', methods=['POST'])
def send_otp():
    user_email = request.form.get('email')
    otp = generate_otp()

    session['otp'] = otp
    session['otp_expiration'] = datetime.now() + timedelta(minutes=10)

    send_otp_email(user_email, otp)

    flash('OTP sent to your email. Please verify.', 'info')
    return redirect(url_for('verify_otp_page'))  

@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    user_input_otp = request.form.get('otp')
    stored_otp = session.get('otp')
    otp_expiration = session.get('otp_expiration')

    if otp_expiration and datetime.now() > otp_expiration:
        flash('OTP has expired. Please request a new one.', 'danger')
        return redirect(url_for('send_otp_page'))

    if user_input_otp == stored_otp:
        session.pop('otp', None)
        session.pop('otp_expiration', None)
        flash('Email verified successfully!', 'success')
        return redirect(url_for('home'))  
    else:
        flash('Invalid OTP. Please try again.', 'danger')
        return redirect(url_for('verify_otp_page'))  

@app.route('/screening', methods=['GET', 'POST'])
@login_required
def screening():
    form = ScreeningForm()
    if form.validate_on_submit():
        province = form.province.data
        if province == "Western Cape":
            flash('You are part of the target population.', 'success')
            return redirect(url_for('submit_demographic'))
        else:
            flash('You are not part of the target population. Thank you for your time.', 'info')
            return redirect(url_for('not_targeted'))
    return render_template('screening.html', form=form)

@app.route('/submit-demographic', methods=['GET', 'POST'])
@login_required
def submit_demographic():
    form = DemographicForm()
    if form.validate_on_submit():
        demographic_response = Demographic(
            user_id=current_user.id,
            registered_name=form.registered_name.data,
            province=form.province.data,
            district=form.district.data,
            municipality=form.municipality.data,
            agricultural_activity=",".join(form.agricultural_activity.data),
            other_agricultural_activity=form.other_agricultural_activity.data,
            farm_activity=",".join(form.farm_activity.data)
        )
        db.session.add(demographic_response)
        db.session.commit()
        
        
        selected_activities = form.agricultural_activity.data
        if 'farming' in selected_activities:
            session['demographics_farming_selected'] = True
            return redirect(url_for('survey'))
        elif 'forestry' in selected_activities:
            session['demographics_farming_selected'] = False
            return redirect(url_for('survey'))
        else:
            return redirect(url_for('home'))
    
    return render_template('demographics.html', form=form)

@app.route('/survey', methods=['GET', 'POST'])
@login_required
def survey():
    form = SurveyForm()
    if form.validate_on_submit():
        survey_response = Survey(
            user_id=current_user.id,
            crops_own=Decimal(form.crops_own.data or 0),
            crops_govt=Decimal(form.crops_govt.data or 0),
            crops_traditional=Decimal(form.crops_traditional.data or 0),
            crops_other=Decimal(form.crops_other.data or 0),
            pastures_own=Decimal(form.pastures_own.data or 0),
            pastures_govt=Decimal(form.pastures_govt.data or 0),
            pastures_traditional=Decimal(form.pastures_traditional.data or 0),
            pastures_other=Decimal(form.pastures_other.data or 0),
            greenhouses_own=Decimal(form.greenhouses_own.data or 0),
            greenhouses_govt=Decimal(form.greenhouses_govt.data or 0),
            greenhouses_traditional=Decimal(form.greenhouses_traditional.data or 0),
            greenhouses_other=Decimal(form.greenhouses_other.data or 0),
            natural_forest_own=Decimal(form.natural_forest_own.data or 0),
            natural_forest_govt=Decimal(form.natural_forest_govt.data or 0),
            natural_forest_traditional=Decimal(form.natural_forest_traditional.data or 0),
            natural_forest_other=Decimal(form.natural_forest_other.data or 0),
            woodland_own=Decimal(form.woodland_own.data or 0),
            woodland_govt=Decimal(form.woodland_govt.data or 0),
            woodland_traditional=Decimal(form.woodland_traditional.data or 0),
            woodland_other=Decimal(form.woodland_other.data or 0),
          
        )
        db.session.add(survey_response)
        db.session.commit()

        if session.get('demographics_farming_selected'):
            return redirect(url_for('field_horticultural_crops'))
        else:
            return redirect(url_for('thank_you'))
    return render_template('survey.html', form=form)

@app.route('/field-horticultural-crops', methods=['GET', 'POST'])
@login_required
def field_horticultural_crops():
    form = FieldHorticulturalCropsForm()
    if form.validate_on_submit():
        field_horticultural_crops_response = FieldHorticulturalCrops(
            user_id=current_user.id,
            farming_practice=",".join(form.farming_practice.data),
            water_supply=",".join(form.water_supply.data),
            irrigation_system=",".join(form.irrigation_system.data)
        )
        db.session.add(field_horticultural_crops_response)
        db.session.commit()

        return redirect(url_for('thank_you'))
    return render_template('field_horticultural_crops.html', form=form)

@app.route('/thank_you')
@login_required
def thank_you():
    return render_template('thank_you.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/not_targeted')
def not_targeted():
    return render_template('not_targeted.html')



if __name__ == '__main__':
    app.run(debug= True)

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateTimeField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from models import db, User, BikeType, Reservation
from datetime import datetime, timedelta
from sqlalchemy import or_
from flask_cors import CORS
from dotenv import load_dotenv
from email_validator import validate_email, EmailNotValidError
import os

# =====================
# ENV & APP CONFIG
# =====================
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback-secret-key')

database_url = os.getenv('DATABASE_URL', 'sqlite:///bikerental.db')
# Fix Render postgres:// -> postgresql://
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
CORS(app, supports_credentials=True)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# =====================
# UTILS
# =====================
def is_valid_email(email: str) -> bool:
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False


def format_currency(value):
    try:
        v = float(value)
        return f"{int(round(v)):,}".replace(',', ' ')
    except Exception:
        return value


app.jinja_env.filters['currency'] = format_currency


# =====================
# FORMS
# =====================
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=150)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


class ReservationForm(FlaskForm):
    bike_type_id = SelectField('Bike Type', coerce=int, validators=[DataRequired()])
    start_date = DateTimeField('Start Date', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    end_date = DateTimeField('End Date', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    submit = SubmitField('Reserve')


# =====================
# ROUTES HTML
# =====================
@app.route('/')
def home():
    bikes = BikeType.query.filter_by(available=True).all()
    return render_template('index.html', bikes=bikes)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        flash('Invalid username or password')
    return render_template('login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if not is_valid_email(form.email.data):
            flash('Email invalide')
            return redirect(url_for('register'))

        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists')
            return redirect(url_for('register'))

        if User.query.filter_by(email=form.email.data).first():
            flash('Email already exists')
            return redirect(url_for('register'))

        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/reserve/<int:bike_id>', methods=['GET', 'POST'])
@login_required
def reserve(bike_id):
    bike = BikeType.query.get_or_404(bike_id)
    form = ReservationForm()
    form.bike_type_id.choices = sorted(
        [(b.id, b.name) for b in BikeType.query.filter_by(available=True).all()],
        key=lambda x: x[1]
    )
    form.bike_type_id.data = bike_id

    if form.validate_on_submit():
        start = form.start_date.data
        end = form.end_date.data

        if start >= end:
            flash('End date must be after start date')
            return redirect(url_for('reserve', bike_id=bike_id))

        if start < datetime.utcnow():
            flash('Start date must be in the future')
            return redirect(url_for('reserve', bike_id=bike_id))

        if end - start > timedelta(days=7):
            flash('Reservation cannot be longer than 7 days')
            return redirect(url_for('reserve', bike_id=bike_id))

        overlapping = Reservation.query.filter(
            Reservation.bike_type_id == bike_id,
            or_(
                Reservation.start_date.between(start, end),
                Reservation.end_date.between(start, end),
                (Reservation.start_date <= start) & (Reservation.end_date >= end)
            )
        ).first()

        if overlapping:
            flash('This bike is already reserved for this period')
            return redirect(url_for('reserve', bike_id=bike_id))

        reservation = Reservation(
            user_id=current_user.id,
            bike_type_id=bike_id,
            start_date=start,
            end_date=end
        )
        db.session.add(reservation)
        db.session.commit()
        flash('Reservation successful')
        return redirect(url_for('dashboard'))

    return render_template('reserve.html', form=form, bike=bike)


@app.route('/dashboard')
@login_required
def dashboard():
    reservations = Reservation.query.filter_by(user_id=current_user.id).all()
    return render_template('user_dashboard.html', reservations=reservations)


@app.route('/about')
def about():
    return render_template('about.html')


# =====================
# ADMIN
# =====================
@app.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        flash('Access denied')
        return redirect(url_for('home'))
    bikes = BikeType.query.all()
    reservations = Reservation.query.all()
    return render_template('admin.html', bikes=bikes, reservations=reservations)


@app.route('/admin/add_bike', methods=['POST'])
@login_required
def add_bike():
    if not current_user.is_admin:
        return jsonify({'error': 'Access denied'}), 403

    data = request.get_json() or {}
    name = data.get('name', '').strip()
    description = data.get('description', '').strip()
    image_url = data.get('image_url') or 'https://source.unsplash.com/400x300/?bicycle'

    try:
        price = float(data.get('price', 0))
    except (TypeError, ValueError):
        return jsonify({'error': 'Invalid price'}), 400

    if not name:
        return jsonify({'error': 'Name required'}), 400

    bike = BikeType(name=name, description=description, price_per_hour=price, image_url=image_url)
    db.session.add(bike)
    db.session.commit()
    return jsonify({'success': True})


# =====================
# API
# =====================
@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json() or {}
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')

    if not username or not email or not password:
        return jsonify({'error': 'missing_fields'}), 400

    if not is_valid_email(email):
        return jsonify({'error': 'invalid_email'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'username_exists'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'email_exists'}), 400

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'success': True})


@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json() or {}
    user = User.query.filter_by(username=data.get('username', '')).first()

    if not user or not user.check_password(data.get('password', '')):
        return jsonify({'error': 'invalid_credentials'}), 401

    login_user(user)
    return jsonify({'success': True})


@app.route('/api/logout', methods=['POST'])
@login_required
def api_logout():
    logout_user()
    return jsonify({'success': True})


# =====================
# INIT DB
# =====================
with app.app_context():
    db.create_all()

    if not User.query.filter_by(username='admin').first():
        admin_password = os.getenv('ADMIN_PASSWORD', 'change-me')
        admin = User(username='admin', email='admin@example.com', is_admin=True)
        admin.set_password(admin_password)
        db.session.add(admin)
        db.session.commit()


# =====================
# RUN
# =====================
if __name__ == "__main__":
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=debug)

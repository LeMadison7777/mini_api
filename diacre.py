from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask import send_from_directory
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateTimeField, SelectField
try:
    from wtforms.validators import DataRequired, Email, EqualTo, Length
except ImportError:
    raise ImportError("WTForms is not installed or cannot be resolved. Install it with: pip install WTForms")
from models import db, User, BikeType, Reservation
from datetime import datetime, timedelta
import os
from sqlalchemy import or_
from markupsafe import Markup
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bikerental.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
# allow frontend dev server to send cookies (credentials)
CORS(app, supports_credentials=True)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Jinja filter for currency formatting
def format_currency(value):
    try:
        v = float(value)
    except Exception:
        return value
    # format with thousands separator, no decimals
    return f"{int(round(v)):,}".replace(',', ' ')

app.jinja_env.filters['currency'] = format_currency

# Forms
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

# Routes
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
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            flash('Username already exists')
            return redirect(url_for('register'))
        user = User.query.filter_by(email=form.email.data).first()
        if user:
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
    # Provide sorted choices for better UX
    form.bike_type_id.choices = sorted([(b.id, b.name) for b in BikeType.query.filter_by(available=True).all()], key=lambda x: x[1])
    form.bike_type_id.data = bike_id
    if form.validate_on_submit():
        start = form.start_date.data
        end = form.end_date.data
        # Basic validations
        if start >= end:
            flash('End date must be after start date')
            return redirect(url_for('reserve', bike_id=bike_id))
        if start < datetime.utcnow():
            
            flash('Start date must be in the future')
            return redirect(url_for('reserve', bike_id=bike_id))
        # Limit maximum reservation length to 7 days to prevent accidental long bookings
        if end - start > timedelta(days=7):
            flash('Reservation cannot be longer than 7 days')
            return redirect(url_for('reserve', bike_id=bike_id))
        # Check for overlapping reservations for the same bike type
        overlapping = Reservation.query.filter(
            Reservation.bike_type_id == form.bike_type_id.data,
            or_(
                Reservation.start_date.between(start, end),
                Reservation.end_date.between(start, end),
                (Reservation.start_date <= start) & (Reservation.end_date >= end)
            )
        ).first()
        if overlapping:
            flash('This bike is already reserved during the selected time period')
            return redirect(url_for('reserve', bike_id=bike_id))
        reservation = Reservation(user_id=current_user.id, bike_type_id=form.bike_type_id.data, start_date=start, end_date=end)
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
    # Basic validation / sanitization
    name = data.get('name', '').strip()
    description = data.get('description', '').strip() if data.get('description') else ''
    try:
        price = float(data.get('price', 0))
    except (TypeError, ValueError):
        return jsonify({'error': 'Invalid price'}), 400
    image_url = data.get('image_url') or 'https://source.unsplash.com/400x300/?bicycle'
    if not name:
        return jsonify({'error': 'Name is required'}), 400
    bike = BikeType(name=name, description=description, price_per_hour=price, image_url=image_url)
    db.session.add(bike)
    db.session.commit()
    return jsonify({'success': True})


### API endpoints for frontend (JSON)
@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json() or {}
    username = data.get('username','').strip()
    email = data.get('email','').strip()
    password = data.get('password','')
    if not username or not email or not password:
        return jsonify({'error':'missing_fields'}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({'error':'username_exists'}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({'error':'email_exists'}), 400
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'success': True})


@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json() or {}
    username = data.get('username','')
    password = data.get('password','')
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({'error':'invalid_credentials'}), 401
    login_user(user)
    return jsonify({'success': True})


@app.route('/api/logout', methods=['POST'])
def api_logout():
    logout_user()
    return jsonify({'success': True})


@app.route('/api/reservations', methods=['POST'])
@login_required
def api_create_reservation():
    data = request.get_json() or {}
    bike_id = data.get('bike_id')
    start = data.get('start')
    end = data.get('end')
    if not bike_id or not start or not end:
        return jsonify({'error':'missing_fields'}), 400
    try:
        start_dt = datetime.fromisoformat(start)
        end_dt = datetime.fromisoformat(end)
    except Exception:
        return jsonify({'error':'invalid_date_format'}), 400
    if start_dt >= end_dt:
        return jsonify({'error':'invalid_range'}), 400
    if start_dt < datetime.utcnow():
        return jsonify({'error':'start_in_past'}), 400
    if end_dt - start_dt > timedelta(days=7):
        return jsonify({'error':'too_long'}), 400
    # overlap check
    overlapping = Reservation.query.filter(
        Reservation.bike_type_id == bike_id,
        or_(
            Reservation.start_date.between(start_dt, end_dt),
            Reservation.end_date.between(start_dt, end_dt),
            (Reservation.start_date <= start_dt) & (Reservation.end_date >= end_dt)
        )
    ).first()
    if overlapping:
        return jsonify({'error':'overlap'}), 400
    reservation = Reservation(user_id=current_user.id, bike_type_id=bike_id, start_date=start_dt, end_date=end_dt)
    db.session.add(reservation)
    db.session.commit()
    return jsonify({'success': True, 'reservation_id': reservation.id})


@app.route('/api/my_reservations')
@login_required
def api_my_reservations():
    res = Reservation.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        'id': r.id,
        'bike_id': r.bike_type_id,
        'start': r.start_date.isoformat(),
        'end': r.end_date.isoformat()
    } for r in res])


@app.route('/api/me')
def api_me():
    if current_user.is_authenticated:
        return jsonify({'authenticated': True, 'username': current_user.username, 'is_admin': current_user.is_admin})
    return jsonify({'authenticated': False})

# API for bikes
@app.route('/api/bikes')
def api_bikes():
    bikes = BikeType.query.filter_by(available=True).all()
    return jsonify([{
        'id': b.id,
        'name': b.name,
        'description': b.description,
        'price_per_hour': b.price_per_hour,
        'currency': 'FCFA',
        'image_url': (request.url_root.rstrip('/') + b.image_url) if b.image_url and b.image_url.startswith('/') else b.image_url
    } for b in bikes])


# Serve React production build if present
FRONTEND_DIST = os.path.join(os.path.dirname(__file__), 'frontend', 'dist')

@app.route('/app/')
@app.route('/app/<path:path>')
def react_app(path=''):
    # if dist exists, serve index or asset
    if os.path.exists(FRONTEND_DIST):
        if path and os.path.exists(os.path.join(FRONTEND_DIST, path)):
            return send_from_directory(FRONTEND_DIST, path)
        # default to index.html
        return send_from_directory(FRONTEND_DIST, 'index.html')
    # fallback to server-rendered home if build not present
    return render_template('index.html')

# Redirect root to React app (if present) for convenience
@app.route('/')
def root():
    if os.path.exists(FRONTEND_DIST):
        return redirect('/app/')
    return render_template('index.html')

# Initialize DB
with app.app_context():
    db.create_all()
    
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', email='admin@example.com', is_admin=True)
        admin.set_password('admin')
        db.session.add(admin)
        db.session.commit()
    
    if not BikeType.query.first():
        bikes = [
            BikeType(
                name="VTT",
                description="Vélo tout terrain pour aventures",
                price_per_hour=15,
                image="velo5.jpg"
            ),
            BikeType(
                name="Vélo Électrique",
                description="Pour rouler sans effort",
                price_per_hour=25,
                image="velo_electrique.jpg"
            ),
            BikeType(
                name="Vélo Route",
                description="Vitesse et performance",
                price_per_hour=20,
                image="velo_route.jpg"
            ),
            BikeType(
                name="Vélo Urbain",
                description="Pour se déplacer en ville",
                price_per_hour=12,
                image="velo5.jpg"
            ),
        ]
        db.session.bulk_save_objects(bikes)  # ✅ Dans le if
        db.session.commit()                   # ✅ Dans le if

if __name__ == "__main__":
    app.run(debug=True)
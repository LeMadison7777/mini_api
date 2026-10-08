from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(150),
        unique=True,
        nullable=False,
        index=True
    )

    email = db.Column(
        db.String(150),
        unique=True,
        nullable=False,
        index=True
    )

    password_hash = db.Column(
        db.String(256),
        nullable=False
    )

    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"


class BikeType(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)

    price_per_hour = db.Column(db.Float, nullable=False)

    image_url = db.Column(
        db.String(255),
        nullable=False
    )

    available = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"<BikeType {self.name}>"


class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
    )

    bike_type_id = db.Column(
        db.Integer,
        db.ForeignKey('bike_type.id'),
        nullable=False
    )

    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    user = db.relationship('User', backref='reservations')
    bike_type = db.relationship('BikeType', backref='reservations')

    def __repr__(self):
        return f"<Reservation user={self.user_id} bike={self.bike_type_id}>"

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app, db
from models import User, BikeType, Reservation
from datetime import datetime, timedelta

def test_user_and_reservation():
    with app.app_context():
        # create a test user
        user = User.query.filter_by(username='pytest_user').first()
        if not user:
            user = User(username='pytest_user', email='pytest@example.com')
            user.set_password('pytestpass')
            db.session.add(user)
            db.session.commit()

        # ensure a bike exists
        bike = BikeType.query.first()
        assert bike is not None

        # create a reservation
        start = datetime.utcnow() + timedelta(days=1)
        end = start + timedelta(hours=2)
        res = Reservation(user_id=user.id, bike_type_id=bike.id, start_date=start, end_date=end)
        db.session.add(res)
        db.session.commit()

        # fetch and assert
        fetched = Reservation.query.filter_by(user_id=user.id, bike_type_id=bike.id).first()
        assert fetched is not None
        assert fetched.start_date == start
        # cleanup
        db.session.delete(fetched)
        db.session.commit()

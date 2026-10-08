"""Small helper to update BikeType.image_url to local static images.
Run with the project venv activated: `python scripts/apply_local_images.py`
"""
from models import db, BikeType
from app import app

MAPPING = {
    'VTT': '/static/img/vtt.jpg',
    'Vélo Électrique': '/static/img/electrique.jpg',
    'Vélo Route': '/static/img/route.jpg',
    'Vélo Urbain': '/static/img/urbain.jpg',
}

with app.app_context():
    for name, path in MAPPING.items():
        bike = BikeType.query.filter_by(name=name).first()
        if bike:
            bike.image_url = path
            print(f"Updated {name} -> {path}")
    db.session.commit()
    print('Done')

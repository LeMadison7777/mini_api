import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app, db
from models import BikeType

local_map = {
    'VTT': 'static/img/velo-vtt.jpg',
    'Vélo Électrique': 'static/img/velo5.jpg',
    'Vélo Route': 'static/img/velo3jpg',
    'Vélo Urbain': 'static/img/velo4.jpg',
}
svg_map = {
    'VTT': 'static/img/velo-vtt.jpg',
    'Vélo Électrique': 'static/img/velo5.jpg',
    'Vélo Route': 'static/img/velo3jpg',
    'Vélo Urbain': 'static/img/velo4.jpg',
}

with app.app_context():
    for name, local_path in local_map.items():
        b = BikeType.query.filter(BikeType.name.ilike(name)).first()
        if not b:
            continue
        # prefer svg local files
        svg_local = svg_map.get(name)
        abs_svg = os.path.join(os.path.dirname(__file__), '..', svg_local) if svg_local else None
        if abs_svg and os.path.exists(abs_svg):
            b.image_url = '/' + svg_local.replace('\\', '/')
            print('Set local SVG image for', b.name, '->', b.image_url)
            continue
        abs_local = os.path.join(os.path.dirname(__file__), '..', local_path)
        if os.path.exists(abs_local):
            b.image_url = '/' + local_path.replace('\\', '/')
            print('Set local image for', b.name, '->', b.image_url)
        else:
            # fallback to a stable picsum image sized 400x300
            fallback = 'https://picsum.photos/400/300?random=' + str(b.id)
            b.image_url = fallback
            print('Set fallback image for', b.name, '->', fallback)
    db.session.commit()
    print('Done')

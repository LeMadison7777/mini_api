from flask import Flask, render_template_string, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bikerental.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ----------------------
# Modèles
# ----------------------
class BikeType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price_per_hour = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    available = db.Column(db.Boolean, default=True)

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bike_type_id = db.Column(db.Integer, db.ForeignKey('bike_type.id'))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)

# ----------------------
# Initialisation DB
# ----------------------
with app.app_context():
    db.create_all()
    if not BikeType.query.first():
        bikes = [
            BikeType(name="VTT", description="Vélo tout terrain pour aventures", price_per_hour=15, image_url="https://picsum.photos/200?random=1"),
            BikeType(name="Vélo Électrique", description="Pour rouler sans effort", price_per_hour=25, image_url="https://picsum.photos/200?random=2"),
            BikeType(name="Vélo Route", description="Vitesse et performance", price_per_hour=20, image_url="https://picsum.photos/200?random=3"),
            BikeType(name="Vélo Urbain", description="Pour se déplacer en ville", price_per_hour=12, image_url="https://picsum.photos/200?random=4"),
        ]
        db.session.bulk_save_objects(bikes)
        db.session.commit()

# ----------------------
# Page HTML + CSS + JS
# ----------------------
HTML_PAGE = """
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<title>Location de Vélos 2025</title>
<style>
body { font-family: Arial, sans-serif; margin:0; padding:0; background:#f7f7f7; }
header { background:#1abc9c; color:white; padding:20px; text-align:center; }
header h1 { margin:0; font-size:2.5em; }
.container { max-width:1200px; margin:20px auto; padding:0 20px; }
.grid { display:grid; grid-template-columns: repeat(auto-fit, minmax(250px,1fr)); gap:20px; }
.card { background:white; border-radius:10px; overflow:hidden; box-shadow:0 5px 15px rgba(0,0,0,0.1); transition:transform 0.2s; }
.card:hover { transform:translateY(-5px); }
.card img { width:100%; height:200px; object-fit:cover; }
.card-content { padding:15px; }
.card-content h3 { margin:0 0 10px 0; }
.card-content p { margin:0 0 15px 0; }
.card-content button { background:#1abc9c; color:white; border:none; padding:10px 15px; border-radius:5px; cursor:pointer; transition:background 0.2s; }
.card-content button:hover { background:#16a085; }
footer { text-align:center; padding:20px; background:#2c3e50; color:white; margin-top:30px; }
#reservation-message { margin:20px 0; text-align:center; font-weight:bold; color:#e74c3c; }
form { margin-top:10px; display:flex; flex-direction:column; gap:10px; }
input[type=datetime-local] { padding:8px; }
</style>
</head>
<body>
<header>
    <h1>🚴 Location de Vélos 2025</h1>
</header>
<div class="container">
    <div class="grid" id="bike-list"></div>
    <div id="reservation-message"></div>
</div>
<footer>
    &copy; 2025 BikeRental. Tous droits réservés.
</footer>

<script>
async function loadBikes() {
    const response = await fetch("/biketypes");
    const bikes = await response.json();
    const bikeList = document.getElementById("bike-list");
    bikeList.innerHTML = "";
    bikes.forEach(bike => {
        const card = document.createElement("div");
        card.className = "card";
        card.innerHTML = `
            <img src="${bike.image_url}" alt="${bike.name}">
            <div class="card-content">
                <h3>${bike.name}</h3>
                <p>${bike.description}</p>
                <p>Prix: ${bike.price_per_hour} €/heure</p>
                <form onsubmit="reserveBike(event, ${bike.id})">
                    <input type="datetime-local" name="start_date" required>
                    <input type="datetime-local" name="end_date" required>
                    <button type="submit">Louer</button>
                </form>
            </div>
        `;
        bikeList.appendChild(card);
    });
}

async function reserveBike(event, bike_id) {
    event.preventDefault();
    const form = event.target;
    const start = form.start_date.value;
    const end = form.end_date.value;
    const response = await fetch("/reserve", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({bike_type_id: bike_id, start_date: start, end_date: end})
    });
    const result = await response.json();
    const messageDiv = document.getElementById("reservation-message");
    if(result.success){
        messageDiv.style.color = "#27ae60";
        messageDiv.innerText = "✅ Vélo réservé avec succès !";
    } else {
        messageDiv.style.color = "#e74c3c";
        messageDiv.innerText = "❌ " + result.error;
    }
    setTimeout(()=>{messageDiv.innerText="";},3000);
}

loadBikes();
</script>
</body>
</html>
"""

# ----------------------
# Routes Flask
# ----------------------
@app.route("/")
def home():
    return render_template_string(HTML_PAGE)

@app.route("/biketypes")
def get_biketypes():
    bikes = BikeType.query.all()
    return jsonify([{
        "id": b.id,
        "name": b.name,
        "description": b.description,
        "price_per_hour": b.price_per_hour,
        "image_url": b.image_url,
        "available": b.available
    } for b in bikes])

@app.route("/reserve", methods=["POST"])
def reserve_bike():
    data = request.get_json()
    bike_type_id = data.get("bike_type_id")
    start_date = data.get("start_date")
    end_date = data.get("end_date")
    bike = BikeType.query.get(bike_type_id)
    if not bike:
        return jsonify({"success": False, "error": "Vélo introuvable"})
    try:
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
        if start >= end:
            return jsonify({"success": False, "error": "Date de fin doit être après la date de début"})
    except:
        return jsonify({"success": False, "error": "Format de date invalide"})
    reservation = Reservation(bike_type_id=bike_type_id, start_date=start, end_date=end)
    db.session.add(reservation)
    db.session.commit()
    return jsonify({"success": True})

# ----------------------
# Lancer l'application
# ----------------------
if __name__ == "__main__":
    app.run(debug=True)

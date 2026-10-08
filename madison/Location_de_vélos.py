from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# Liste de vélos disponibles
bikes = [
    {"id": 1, "name": "Vélo Route 3000", "price": 15, "img": "https://picsum.photos/200?random=1"},
    {"id": 2, "name": "VTT Montagne", "price": 20, "img": "https://picsum.photos/200?random=2"},
    {"id": 3, "name": "Vélo Électrique", "price": 25, "img": "https://picsum.photos/200?random=3"},
    {"id": 4, "name": "Vélo Urbain", "price": 12, "img": "https://picsum.photos/200?random=4"}
]

# Stockage des réservations
reservations = []

# Page HTML + CSS + JS intégrée
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
    const response = await fetch("/bikes");
    const bikes = await response.json();
    const bikeList = document.getElementById("bike-list");
    bikeList.innerHTML = "";
    bikes.forEach(bike => {
        const card = document.createElement("div");
        card.className = "card";
        card.innerHTML = `
            <img src="${bike.img}" alt="${bike.name}">
            <div class="card-content">
                <h3>${bike.name}</h3>
                <p>Prix: ${bike.price} €/heure</p>
                <button onclick="reserveBike(${bike.id})">Louer</button>
            </div>
        `;
        bikeList.appendChild(card);
    });
}

async function reserveBike(id) {
    const response = await fetch("/reserve", {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({bike_id: id})
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

@app.route("/")
def home():
    return render_template_string(HTML_PAGE)

@app.route("/bikes")
def get_bikes():
    return jsonify(bikes)

@app.route("/reserve", methods=["POST"])
def reserve_bike():
    data = request.get_json()
    bike_id = data.get("bike_id")
    bike = next((b for b in bikes if b["id"] == bike_id), None)
    if not bike:
        return jsonify({"success": False, "error": "Vélo introuvable"})
    reservations.append(bike)
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(debug=True)

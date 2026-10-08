from flask import Flask, render_template

app = Flask(__name__)

# Liste des vélos
bikes = [
    {"name": "VTT", "description": "Vélo tout terrain pour aventures", "price": 15, "image": "/static/images/velo1.jpg"},
    {"name": "Vélo Électrique", "description": "Pour rouler sans effort", "price": 25, "image": "/static/images/velo2.jpg"},
    {"name": "Vélo Route", "description": "Vitesse et performance", "price": 20, "image": "/static/images/velo3.jpg"},
    {"name": "Vélo Urbain", "description": "Pour se déplacer en ville", "price": 12, "image": "/static/images/velo4.jpg"},
]

@app.route("/")
def home():
    return render_template("index.html", bikes=bikes)

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, jsonify, request

app = Flask(__name__)

# EXO 1 : API GET
@app.route("/api/salutation", methods=["GET"])
def salutation():
    return jsonify(message="Hello World")

# EXO 2 : API POST
@app.route("/api/utilisateurs", methods=["POST"])
def utilisateurs():
    data = request.get_json()      # récupérer le JSON envoyé
    nom = data.get("nom")          # récupérer le champ "nom"

    return jsonify(message=f"Bonjour {nom}")

if __name__ == '__main__':
    app.run(debug=True)


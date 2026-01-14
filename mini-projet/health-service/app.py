from flask import Flask, request, jsonify
import json
import requests
from functools import wraps

app = Flask(__name__)
AUTH_SERVICE_URL = "http://localhost:5000/verify"
PERSON_SERVICE_URL = "http://localhost:5001/persons/"

DATA_FILE = "data.json"

# ---------------- JWT via Auth-Service ----------------
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token manquant'}), 401
        r = requests.post(AUTH_SERVICE_URL, json={'token': token})
        if r.status_code != 200:
            return jsonify({'message': 'Token invalide'}), 401
        return f(*args, **kwargs)
    return decorated

# ---------------- Utils ----------------
def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def person_exists(person_id, token):
    r = requests.get(PERSON_SERVICE_URL + str(person_id), headers={"Authorization": token})
    return r.status_code == 200

# ---------------- API Health ----------------
@app.route('/health/<int:person_id>', methods=['GET'])
@token_required
def get_health(person_id):
    token = request.headers.get('Authorization')
    if not person_exists(person_id, token):
        return jsonify({'message': 'Personne inexistante'}), 404
    data = load_data()
    return jsonify(data.get(str(person_id), {}))

@app.route('/health/<int:person_id>', methods=['POST', 'PUT'])
@token_required
def add_or_update_health(person_id):
    token = request.headers.get('Authorization')
    if not person_exists(person_id, token):
        return jsonify({'message': 'Personne inexistante'}), 404
    data = load_data()
    data[str(person_id)] = request.json
    save_data(data)
    return jsonify({'message': 'Données de santé enregistrées'})

@app.route('/health/<int:person_id>', methods=['DELETE'])
@token_required
def delete_health(person_id):
    data = load_data()
    data.pop(str(person_id), None)
    save_data(data)
    return jsonify({'message': 'Données de santé supprimées'})

if __name__ == '__main__':
    app.run(port=5002)

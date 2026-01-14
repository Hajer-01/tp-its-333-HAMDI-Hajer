from flask import Flask, request, jsonify
import sqlite3
import requests
from functools import wraps

app = Flask(__name__)
AUTH_SERVICE_URL = "http://localhost:5000/verify"

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

# ---------------- Database ----------------
def get_db():
    conn = sqlite3.connect("database.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS person (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)
    return conn

# ---------------- API Person ----------------
@app.route('/persons', methods=['POST'])
@token_required
def create_person():
    data = request.json
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO person (name) VALUES (?)", (data['name'],))
    conn.commit()
    person_id = cur.lastrowid
    conn.close()
    return jsonify({'id': person_id, 'name': data['name']}), 201

@app.route('/persons/<int:id>', methods=['GET'])
@token_required
def get_person(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM person WHERE id=?", (id,))
    person = cur.fetchone()
    conn.close()
    if person:
        return jsonify({'id': person[0], 'name': person[1]})
    return jsonify({'message': 'Personne inexistante'}), 404

@app.route('/persons/<int:id>', methods=['DELETE'])
@token_required
def delete_person(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM person WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Personne supprimée'})

if __name__ == '__main__':
    app.run(port=5001)

from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# =======================
# Initialisation BD
# =======================
def init_db():
    conn = sqlite3.connect("database.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS etudiants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            adresse TEXT NOT NULL,
            pin TEXT NOT NULL
        )
    """)
    conn.close()

# =======================
# Connexion BD
# =======================
def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# =======================
# Routes
# =======================

# Afficher la liste des étudiants
@app.route("/")
def list_students():
    conn = get_db_connection()
    etudiants = conn.execute("SELECT * FROM etudiants").fetchall()
    conn.close()
    return render_template("list.html", etudiants=etudiants)

# Ajouter un étudiant
@app.route("/new", methods=["GET", "POST"])
def new_student():
    if request.method == "POST":
        nom = request.form["nom"]
        adresse = request.form["adresse"]
        pin = request.form["pin"]

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO etudiants (nom, adresse, pin) VALUES (?, ?, ?)",
            (nom, adresse, pin)
        )
        conn.commit()
        conn.close()

        return redirect(url_for("list_students"))

    return render_template("new.html")

# =======================
# Lancement app
# =======================
if __name__ == "__main__":
    init_db()
    app.run(debug=True)



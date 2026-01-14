from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# ==========================
# Configuration SQLite
# ==========================
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ==========================
# MODELS
# ==========================

class Groupe(db.Model):
    __tablename__ = "groupe"

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)

    # Relation 1 -> N
    etudiants = db.relationship("Etudiant", backref="groupe", lazy=True)

    def __repr__(self):
        return f"<Groupe {self.nom}>"

class Etudiant(db.Model):
    __tablename__ = "etudiant"

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(80), nullable=False)
    adresse = db.Column(db.String(120), nullable=False)
    pin = db.Column(db.String(20), nullable=False)

    # Clé étrangère
    group_id = db.Column(db.Integer, db.ForeignKey("groupe.id"))

    def __repr__(self):
        return f"<Etudiant {self.nom}>"

# ==========================
# INITIALISATION & DONNÉES
# ==========================
@app.route("/")
def init_data():
    db.drop_all()
    db.create_all()

    # Création du groupe ITS2
    its2 = Groupe(nom="ITS2")
    db.session.add(its2)
    db.session.commit()

    # Création de 3 étudiants
    e1 = Etudiant(nom="Alice", adresse="Paris", pin="75000", groupe=its2)
    e2 = Etudiant(nom="Bob", adresse="Créteil", pin="94000", groupe=its2)
    e3 = Etudiant(nom="Charlie", adresse="Evry", pin="91000", groupe=its2)

    db.session.add_all([e1, e2, e3])
    db.session.commit()

    return "Groupe ITS2 et 3 étudiants créés avec succès ✅"

# ==========================
# LANCEMENT
# ==========================
if __name__ == "__main__":
    app.run(debug=True)



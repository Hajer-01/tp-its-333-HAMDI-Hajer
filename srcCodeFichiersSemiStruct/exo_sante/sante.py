import json

# Charger le fichier JSON
with open("sante.json", "r", encoding="utf-8") as f:
    sante = json.load(f)

def chercher_sante(nom):
    """
    Cherche les paramètres de santé d'une personne
    et les renvoie sous forme JSON.
    """
    if nom in sante:
        return json.dumps({nom: sante[nom]}, ensure_ascii=False, indent=4)
    else:
        return json.dumps({"erreur": f"Aucune donnée pour {nom}"}, ensure_ascii=False, indent=4)

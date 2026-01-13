import json

# Lire le fichier JSON dans le dossier parent
with open('../data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("AVANT modification :")
print(json.dumps(data["features"], sort_keys=True, indent=4))

# Modifier les données
data["features"][0]["geometry"]["coordinates"] = [78.0, 45.0]
data["features"][0]["properties"]["prop1"] = "value1"

# Écrire dans le fichier JSON dans le dossier parent
with open('../data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("\nAPRÈS modification :")
print(json.dumps(data["features"], sort_keys=True, indent=4))


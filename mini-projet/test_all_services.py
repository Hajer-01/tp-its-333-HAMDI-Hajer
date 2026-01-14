import requests

# ---- Auth-Service ----
auth_url = "http://127.0.0.1:5000/login"
r = requests.post(auth_url)
token = r.json()['token']
print("Token JWT :", token)

headers = {"Authorization": token, "Content-Type": "application/json"}

# ---- Person-Service ----
person_url = "http://127.0.0.1:5001/persons"
data_person = {"name": "Alice"}
r = requests.post(person_url, json=data_person, headers=headers)
person_id = r.json()['id']
print("Person created:", r.json())

# ---- Health-Service ----
health_url = f"http://127.0.0.1:5002/health/{person_id}"
data_health = {"poids": 70, "taille": 175, "frequence_cardiaque": 72}
r = requests.post(health_url, json=data_health, headers=headers)
print("Health added:", r.json())

# ---- Lire les données santé ----
r = requests.get(health_url, headers=headers)
print("Health data:", r.json())

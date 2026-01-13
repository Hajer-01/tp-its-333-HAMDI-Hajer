from sante import chercher_sante

# Test 1 : personne existante
print("Test 1 : Hajer")
resultat = chercher_sante("Hajer")
print(resultat)

# Test 2 : personne inexistante
print("\nTest 2 : Charlie")
resultat2 = chercher_sante("Charlie")
print(resultat2)

import json
import psycopg  # Connexion PostgreSQL

# Connexion à la base
conn = psycopg.connect(
    dbname="",
    user="postgres",
    password="",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Fonction pour importer un fichier JSON
def importJSON(paths):
	with open(paths, "r") as file:
		return json.load(file)

# Fonction de log d’erreur
def journal_erreur(message):
    with open(f"./bdd/error.txt", "a") as fichier:
        fichier.write(message + "\n")

# Initialisation des données
version = []
champ = []
path = {
	"folder" : "./data/"
}

# Chargement de la liste des versions
version = importJSON("./data/version.json")

# TODO : traitement des champions à ajouter ici

conn.commit()      # Valide les changements
cursor.close()     # Ferme le curseur
conn.close()       # Ferme la connexion

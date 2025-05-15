import json
import psycopg

# Connexion PostgreSQL
conn = psycopg.connect(
    dbname="",
    user="postgres",
    password="",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Types de fichiers JSON à insérer
typ = ["champion", "item", "runesReforged", "summoner", "map"]
extra = ""
path = {
	"folder" : f"{extra}./data/"
}

# Chargement de la liste des versions
with open(f"{path['folder']}version.json", "r") as file:
    data = json.load(file)

# Fonction de log d’erreur
def journal_erreur(message):
    with open(f"{extra}./bdd/error.txt", "a") as fichier:
        fichier.write(message + "\n")

# Parcours des versions et types de données
for version in data:
    for t in typ:
        try:
            # Vérifie si la donnée existe déjà
            cursor.execute("SELECT 1 FROM global WHERE ver_name = %s AND name = %s", (version, t))
            result = cursor.fetchone()

            if not result:
                try:
                    with open(f"{path['folder']}version/{version}/{t}.json", "r") as file:
                        json_data = json.load(file)

                    cursor.execute(
                        "INSERT INTO global (ver_name, name, json_data) VALUES (%s, %s, %s)",
                        (version, t, json.dumps(json_data))
                    )
                    print(f"Version {version} {t} ajouté")
                except FileNotFoundError:
                    message = f"Fichier introuvable pour la version {version}, type {t}"
                    journal_erreur(message)
                    print(message)
        except Exception as e:
            message = f"Erreur avec la version {version}, type {t} : {e}"
            print(message)
            journal_erreur(message)
            conn.rollback()

conn.commit()
cursor.close()
conn.close()

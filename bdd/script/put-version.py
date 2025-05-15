import json
import psycopg

# Connexion PostgreSQL
conn = psycopg.connect(
    dbname="",  # À compléter
    user="postgres",
    password="",  # À compléter
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

data = []
extra = ""
path = {
	"folder" : f"{extra}./data/"
}

# Chargement de la liste des versions
with open(f"{path['folder']}version.json", "r") as file:
	data = json.load(file)
data.reverse()  # Insertion dans l'ordre décroissant

# Insertion des versions non existantes
for version in data:
    cursor.execute("SELECT 1 FROM version WHERE ver_name = %s", (version,))
    result = cursor.fetchone()

    if not result:
        cursor.execute("INSERT INTO version (ver_name) VALUES (%s)", (version,))
        print(f"Verison {version} ajouté")

conn.commit()
cursor.close()
conn.close()

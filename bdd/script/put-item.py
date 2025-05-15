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

# Structure de données d’un item
data = {
	"ver_name": "",
	"name" : "",
	"json_data" : {},
	"image" : ""
}
extra = ""
path = {
	"folder" : f"{extra}./data/"
}
n = 0

# Import JSON (utf-8)
def importJSON(paths):
	with open(paths, "r", encoding="utf-8") as file:
		return json.load(file)

# Import binaire d’image
def importImage(paths):
	with open(paths, "rb") as file:
		return file.read()

# Log d’erreur
def journal_erreur(message):
	with open(f"{extra}./bdd/error.txt", "a") as fichier:
		fichier.write(str(message) + "\n")
	print(message)

# Traitement des versions
listVersion = importJSON(f"{path['folder']}version.json")
for version in listVersion:
	try:
		listObjet = importJSON(f"{path['folder']}version/{version}/item.json")
		for objet in listObjet['data']:
			data["ver_name"] = version
			data["name"] = listObjet['data'][objet]['name']
			data["json_data"] = listObjet['data'][objet]
			data["image"] = importImage(f"{path['folder']}version/{version}/item/{objet}.png")

			cursor.execute("SELECT 1 FROM item WHERE ver_name = %s AND name = %s", (data["ver_name"], data["name"]))
			result = cursor.fetchone()

			if not result:
				cursor.execute(
					"INSERT INTO item (ver_name, name, json_data, image) VALUES (%s, %s, %s, %s)",
					(data["ver_name"], data["name"], json.dumps(data["json_data"]), psycopg.Binary(data["image"]))
				)
				print(f"Item {data['name']} ajouté {data['ver_name']}")
				n += 1
	except Exception as e:
		journal_erreur(e)

conn.commit()
cursor.close()
conn.close()

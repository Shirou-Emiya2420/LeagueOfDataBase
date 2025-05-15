""" 🔁 Imports de modules nécessaires """
import requests  # Pour envoyer des requêtes HTTP vers l'API Riot
import json      # Pour sérialiser et désérialiser les données JSON
import os        # Pour gérer les chemins, fichiers et dossiers
import time      # Pour le logging temporel si besoin

""" 🔑 Configuration API Riot """
apiKey = "" #Mettre votre clef ici :)
headers = {
    "X-Riot-Token": apiKey
}

""" 📦 Données globales utilisées dans les fonctions """
n = 0  # Compteur global des requêtes API effectuées

donner = {
    "version": [],  # Liste des versions du jeu
    "data": {
        "champion": {},
        "item": {},
        "runesReforged": {},
        "summoner": {},
        "map": {}
    }
}

""" 🗂️ Chemins des dossiers utilisés dans le projet """
extra = ""  # Ajout dynamique possible (ex: "../")
path = {
    "folder": f"{extra}./data/",             # Dossier principal de stockage des données JSON/images
    "error": "./cron/error.txt",             # Fichier log des erreurs
    "script": "./bdd/"                       # Dossier des scripts Python liés à l’insertion BDD
}

""" 🔤 Configuration des spells (pour nommage Q/W/E/R) """
spell = {
    "inti": ["Q", "W", "E", "R"],  # Ordre des sorts pour nommage
    "index": 0                     # Index courant utilisé pendant l’export des images de sorts
}


def requetAPI(url):
    """
    Envoie une requête GET à l'API Riot et retourne la réponse.

    Args:
        url (str): URL complète de l'API.

    Returns:
        requests.Response | int: Réponse API en cas de succès, -1 sinon.
    """
    global n
    try:
        # Envoi de la requête avec l’en-tête contenant la clé API
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            # Incrémentation du compteur de requêtes réussies
            n += 1
            print(f"API |{n}|")
            return response
        else:
            # Affiche le code d’erreur et le contenu retourné
            print(f"Erreur : {response.status_code} - {response.json()}")
            return -1

    except Exception as e:
        # Capture les erreurs réseau ou inattendues
        print("Une erreur est survenue :", str(e))
        return -1

def requetResult(val):
    """
    Vérifie si le résultat d'une requête est une erreur (valeur -1).

    Args:
        val (requests.Response | int): Retour de la fonction requetAPI.

    Returns:
        bool: True si erreur, False sinon.
    """
    # Si la requête a échoué (renvoie -1), affiche un message d’erreur
    if val == -1:
        print("Récupération des données échouée.")
        return True

    # Sinon, tout s’est bien passé
    return False

def exportJSON(paths, val, files, encod=""):
    """
    Enregistre un dictionnaire JSON dans un fichier texte.

    Args:
        paths (str): Dossier de destination.
        val (dict): Données à sauvegarder.
        files (str): Nom du fichier (ex: "/item.json").
        encod (str): Encodage du fichier (ex: "utf-8").

    Returns:
        str: Message indiquant le succès ou l’échec de l’export.
    """
    # Crée le dossier si besoin
    if not os.path.exists(paths):
        os.makedirs(paths)

    # Écriture du JSON dans le fichier
    with open(paths + files, "w", encoding=encod) as file:
        json.dump(val, file, indent=4, ensure_ascii=False)
        return f"{paths + files} Sauvegardé"

    # Ce return est normalement inutile (inatteignable)
    return f"{paths + files} échoué"

def exportBinaire(paths, val, files):
    """
    Enregistre une ressource binaire (ex: image) sur le disque.

    Args:
        paths (str): Dossier de destination.
        val (requests.Response): Réponse contenant les données binaires.
        files (str): Nom du fichier de sortie.

    Returns:
        str: Message de confirmation ou d’erreur.
    """
    # Crée le dossier si besoin
    if not os.path.exists(paths):
        os.makedirs(paths)

    # Écriture binaire du contenu dans le fichier
    with open(paths + files, "wb") as file:
        file.write(val.content)
        return f"Fichier {paths + files} Sauvegardé"

    # Cas théorique d’échec
    return f"Exportation du fichier {paths + files} échouée !!!!"

def importJSON(paths):
    """
    Importe un fichier JSON en tant qu’objet Python.

    Args:
        paths (str): Chemin du fichier à lire.

    Returns:
        dict | list: Données JSON chargées.
    """
    # Ouvre et lit le fichier JSON
    with open(paths, "r") as file:
        return json.load(file)

def journal_erreur(message):
	"""
    Ajoute un message d'erreur dans un fichier log, et l'affiche.

    Args:
        message (str): Message à enregistrer.
    """
	# Crée le dossier si besoin
	if not os.path.exists(f"{path['folder']}"):
		os.makedirs(f"{path['folder']}")
	# Ouvre ou crée le fichier error.txt en mode ajout
	with open(f"{path['folder']}error.txt", "a") as fichier:
		fichier.write(message + "\n")
	# Affiche le message pour retour console
	print(message) 

def isExisting(chemin):
    """
    Vérifie si un fichier ou un dossier existe à un chemin donné.

    Args:
        chemin (str): Chemin à tester.

    Returns:
        int: 1 si existant, 0 sinon.
    """
    return 1 if os.path.exists(chemin) else 0




def getVersion(save):
    """
    Récupère la liste des versions du jeu depuis l'API Riot.

    Args:
        save (bool): Si True, sauvegarde localement la liste en JSON.

    Returns:
        list | None: Liste des versions ou None si erreur.
    """
    global donner
    url = "https://ddragon.leagueoflegends.com/api/versions.json"

    # Appelle l'API pour récupérer les versions
    result = requetAPI(url)
    if requetResult(result):
        return

    # Stocke le résultat dans les données globales
    donner['version'] = result.json()

    # Sauvegarde locale facultative
    if save:
        print(exportJSON(f"{path['folder']}", donner['version'], "/version.json", "utf-8"))

    return donner['version']

def getData(save, version):
    """
    Récupère les fichiers de données principaux (champions, items, runes, etc.)
    pour une version donnée du jeu.

    Args:
        save (bool): Si True, sauvegarde chaque JSON localement.
        version (str): Version ciblée (ex: "13.6.1").
    """
    global donner
    # Pour chaque type de donnée (champion, item, etc.)
    for val in donner['data']:
        url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/fr_FR/{val}.json"
        result = requetAPI(url)

        if requetResult(result):
            return

        # Sauvegarde locale dans un sous-dossier spécifique
        if save:
            print(exportJSON(f"{path['folder']}version/{version}", result.json(), f"/{val}.json", "utf-8"))



def getChampData(champ, save, version):
    """
    Récupère les données complètes d’un champion spécifique.

    Args:
        champ (str): Nom du champion (ex: "Ahri").
        save (bool): Si True, sauvegarde le fichier localement.
        version (str): Version ciblée.
    
    Returns:
        dict | None: JSON des données du champion ou None si erreur.
    """
    global n

    chemin = f"{path['folder']}/version/{version}/champ/{champ}/{champ}.json"

    # Si déjà existant localement, on le recharge
    if isExisting(chemin):
        print(f"{chemin} existant")
        return importJSON(chemin)

    # Sinon on le récupère depuis l’API
    url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/fr_FR/champion/{champ}.json"
    result = requetAPI(url)

    if requetResult(result):
        return journal_erreur(f"Champion: {champ} Version: {version} ERREUR REQUET |{n}|")

    result = result.json()

    # Sauvegarde locale
    if save:
        print(exportJSON(f"{path['folder']}/version/{version}/champ/{champ}", result, f"/{champ}.json", "utf-8"))

    return result

def getChampMainImg(champ, chemin, version):
    """
    Télécharge l'image principale (icône) d’un champion.

    Args:
        champ (str): Nom du champion.
        chemin (str): Dossier de destination.
        version (str): Version du jeu.
    """
    # Si l’image existe déjà, on ignore
    if isExisting(f"{chemin}{champ}.png"):
        print(f"Fichier {version} {champ}.png existant")
        return

    # Récupère les données du champion localement
    champion = importJSON(f"{path['folder']}/version/{version}/champ/{champ}/{champ}.json")
    image_name = champion['data'][champ]['image']['full']

    # Construit l’URL vers l’image
    url = f"https://ddragon.leagueoflegends.com/cdn/{version}/img/champion/{image_name}"
    result = requetAPI(url)

    if requetResult(result):
        journal_erreur(f"Icone_{champ}.png Erreur")
    else:
        print(exportBinaire(chemin, result, f"{champ}.png"))

def getChampPassiveImg(champ, chemin, version):
    """
    Télécharge l'image du passif d’un champion.

    Args:
        champ (str): Nom du champion.
        chemin (str): Dossier de destination.
        version (str): Version du jeu.
    """
    # Vérifie si l'image existe déjà
    if isExisting(f"{chemin}{champ}_passif.jpg"):
        print(f"Fichier {version} {champ}_passif.jpg existant")
        return

    # Charge les données du champion depuis le fichier JSON
    champJson = importJSON(f"{path['folder']}version/{version}/champ/{champ}/{champ}.json")
    image_name = champJson['data'][champ]['passive']['image']['full']

    # Construit l’URL de l’image
    url = f"https://ddragon.leagueoflegends.com/cdn/{version}/img/passive/{image_name}"
    result = requetAPI(url)

    if requetResult(result):
        journal_erreur(f"Passive_{champ}.jpg Erreur")
    else:
        print(exportBinaire(chemin, result, f"{champ}_passif.jpg"))

def getChampSpellImg(champ, chemin, version):
    """
    Télécharge les images des sorts (Q, W, E, R) d’un champion.

    Args:
        champ (str): Nom du champion.
        chemin (str): Dossier de destination.
        version (str): Version du jeu.
    """
    # Récupère les données complètes du champion
    champJson = importJSON(f"{path['folder']}version/{version}/champ/{champ}/{champ}.json")
    spell['index'] = 0  # Réinitialise l’index de sort (Q, W, E, R)

    for val in champJson['data'][champ]['spells']:
        spell_code = spell['inti'][spell['index']]
        filename = f"{chemin}{champ}_{spell_code}.jpg"

        # Ignore si l’image existe déjà
        if isExisting(filename):
            print(f"Fichier {version} {champ}_{spell_code}.jpg existant")
            spell['index'] += 1
            continue

        # Télécharge l’image du sort
        url = f"https://ddragon.leagueoflegends.com/cdn/{version}/img/spell/{val['image']['full']}"
        result = requetAPI(url)

        if requetResult(result):
            journal_erreur(f"{champ}_{spell_code}.jpg")
        else:
            print(exportBinaire(chemin, result, f"{champ}_{spell_code}.jpg"))

        spell['index'] += 1

def getChampSkinImg(champ, chemin, version):
    """
    Télécharge toutes les images des skins d’un champion.

    Args:
        champ (str): Nom du champion.
        chemin (str): Dossier où stocker les images.
        version (str): Version du jeu.
    """
    # Charge les infos détaillées du champion
    currentChamp = importJSON(f"{path['folder']}/version/{version}/champ/{champ}/{champ}.json")

    for skin in currentChamp['data'][champ]['skins']:
        # Nettoie le nom du skin pour éviter les caractères spéciaux
        skin_name = f"skin_{((skin['name'].replace('/', '_')).replace(' ', '_')).replace(' :', '_')}.jpg"
        skin_path = f"{chemin}{skin_name}"

        if isExisting(skin_path):
            print(f"Fichier {version} {skin_name} existant")
            continue

        # URL officielle de l'image de splash
        url = f"https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{champ}_{skin['num']}.jpg"
        result = requetAPI(url)

        if requetResult(result):
            journal_erreur(f"{skin['name']}.jpg {url} Erreur")
        else:
            print(exportBinaire(chemin, result, skin_name))

def getChampIcone(version):
    """
    Télécharge toutes les icônes, passifs, sorts et skins de chaque champion pour une version.

    Args:
        version (str): Version du jeu ciblée.
    """
    # Récupère la liste des champions pour la version
    champion = importJSON(f"{path['folder']}/version/{version}/champion.json")

    # Pour chaque champion, télécharge les différentes images
    for champ in champion['data']:
        getChampMainImg(champ, f"{path['folder']}/version/{version}/champ/{champ}/", version)
        getChampPassiveImg(champ, f"{path['folder']}/version/{version}/champ/{champ}/", version)
        getChampSpellImg(champ, f"{path['folder']}/version/{version}/champ/{champ}/", version)
        getChampSkinImg(champ, f"{path['folder']}/version/{version}/champ/{champ}/", version)




def getItemImg(version):
    """
    Télécharge toutes les icônes des items pour une version donnée.

    Args:
        version (str): Version ciblée.
    """
    try:
        # Charge les données des items depuis le fichier local
        item = importJSON(f"{path['folder']}version/{version}/item.json")

        for it in item['data']:
            filename = item['data'][it]['image']['full']
            filepath = f"{path['folder']}version/{version}/item/{filename}"

            # Ignore si le fichier existe déjà
            if isExisting(filepath):
                print(f"Fichier {version} {filename} existant")
                continue

            # Construit l'URL de l'image à télécharger
            url = f"https://ddragon.leagueoflegends.com/cdn/{version}/img/item/{filename}"
            result = requetAPI(url)

            if requetResult(result):
                journal_erreur(f"{item['data'][it]['name']}.jpg {url} Erreur")
                print(f"{item['data'][it]['name']}.jpg Erreur")
            else:
                print(exportBinaire(f"{path['folder']}version/{version}/item/", result, filename))
    
    except Exception as e:
        # Capture toute erreur inattendue
        journal_erreur(f"Version: {version} ERREUR ITEM {e} {time.asctime()}")

def getItemAllImg():
    """
    Télécharge les icônes des items pour toutes les versions connues.
    """
    # Charge toutes les versions connues (fichier version.json)
    donner["version"] = importJSON(f"{path['folder']}version.json")

    # Appelle getItemImg pour chaque version
    for version in donner['version']:
        getItemImg(version)



def getDataAllVer():
    """
    Récupère les fichiers de données principaux pour toutes les versions.

    Cela inclut : champions, items, runes, maps, invocateurs.
    """
    # Charge la liste des versions depuis le fichier local
    donner["version"] = importJSON(f"{path['folder']}version.json")

    # Appelle getData pour chaque version
    for ver in donner["version"]:
        getData(True, ver)

def getAllChampData():
    """
    Récupère les données complètes de tous les champions pour chaque version.

    Les données sont stockées en fichiers JSON individuels.
    """
    # Charge les versions depuis le fichier local
    donner["version"] = importJSON(f"{path['folder']}version.json")

    for ver in donner['version']:
        try:
            # Charge la liste des champions pour cette version
            champ = importJSON(f"{path['folder']}/version/{ver}/champion.json")

            # Récupère les données de chaque champion
            for ch in champ['data']:
                getChampData(ch, True, ver)

        except Exception as e:
            # Log l’erreur si un champion échoue
            journal_erreur(f"Version: {ver} ERREUR CHAMPION {e} {ch}")

def getAllChampIcone():
    """
    Télécharge toutes les icônes, sorts, passifs et skins des champions pour toutes les versions.
    """
    # Charge les versions depuis le fichier local
    donner["version"] = importJSON(f"{path['folder']}version.json")

    # Pour chaque version, télécharge les ressources visuelles des champions
    for ver in donner['version']:
        getChampIcone(ver)

def getAllChamp():
    """
    Récupère toutes les données et toutes les icônes des champions
    pour chaque version enregistrée.
    """
    getAllChampData()     # JSON de chaque champion
    getAllChampIcone()    # Images (icône, sort, passif, skin)

#getVersion(True)
#getDataAllVer()
#getAllChamp()
#getItemAllImg()

listScript = [f"{path['script']}put-version.py", f"{path['script']}put-global.py", f"{path['script']}put-item.py"]

for sc in listScript:
	os.system(f"python3 {sc}")
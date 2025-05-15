# League of Legends Data Manager

Ce projet Python permet de récupérer les données officielles de League of Legends via l'API Riot, de les stocker localement ou de les insérer dans une base de données PostgreSQL pour exploitation ultérieure.

## 📚 Fonctionnalités

* Récupération des versions du jeu
* Extraction des données des objets et des champions (JSON + images)
* Insertion directe dans PostgreSQL sans stockage local obligatoire
* Fichier d'erreurs automatique en cas de problème

## 🔹 Structure du projet

```
.gitattributes
README.md

bdd/
├──script/
│   ├──put-champ.py         # Insertion des données complètes des champions
│   ├──put-global.py        # Insertion globale des fichiers JSON (non utilisé ici)
│   ├──put-item.py          # Insertion des objets avec image
│   └──put-version.py       # Insertion des versions dans la table version
└──sql/
    └──table-list.sql        # Définition des tables PostgreSQL

cron/
└──update-data.py         # Script principal de récupération des données Riot

data/
└──script/
    └──libRiotAPI.py         # Fonctions d'appel API, export JSON/image, logging
```

## 🔗 Base de données

Structure PostgreSQL définie dans [`table-list.sql`](bdd/sql/table-list.sql).
Contient les tables suivantes : `version`, `champion`, `item`, `runesReforged`, `summoner`, `map`.

## 🔧 Installation

1. Cloner le dépôt localement
2. Configurer votre base PostgreSQL : créer une base `league_of_legend`
3. Exécuter les scripts `put-*.py` dans `bdd/script` pour insérer les données

> Aucun fichier `requirements.txt` n'est nécessaire : seul `psycopg` est requis.

## ⚖️ Utilisation

* Lancer `update-data.py` pour récupérer les données (champions, objets...)
* Exécuter les scripts `put-champ.py` et `put-item.py` pour remplir la BDD

## 🔍 Fonctions de `libRiotAPI.py`

### 🔗 Fonctions générales

* **`requetAPI(url)`** : Envoie une requête GET à Riot API avec authentification, renvoie la réponse HTTP ou -1 en cas d'erreur.
* **`requetResult(val)`** : Vérifie si la réponse retournée est une erreur (`-1`), utile pour contrôler les appels API.
* **`exportJSON(paths, val, files, encod="")`** : Exporte des données Python en fichier JSON, avec encodage optionnel.
* **`exportBinaire(paths, val, files)`** : Enregistre une réponse binaire (image) sur le disque.
* **`importJSON(paths)`** : Charge un fichier JSON et retourne les données.
* **`journal_erreur(message)`** : Enregistre un message d’erreur dans `error.txt` et l'affiche en console.
* **`isExisting(chemin)`** : Retourne 1 si le chemin existe, 0 sinon.

### 📦 Données et versions

* **`getVersion(save)`** : Récupère la liste des versions disponibles depuis Riot et peut la sauvegarder.
* **`getData(save, version)`** : Récupère les fichiers JSON principaux (champions, objets, runes...) pour une version donnée. *(non utilisé ici)*

### 👤 Fonctions liées aux champions

* **`getChampData(champ, save, version)`** : Récupère les données JSON d’un champion spécifique.
* **`getChampMainImg(champ, chemin, version)`** : Télécharge l’image d’icône du champion.
* **`getChampPassiveImg(champ, chemin, version)`** : Télécharge l’image de la compétence passive du champion.
* **`getChampSpellImg(champ, chemin, version)`** : Télécharge les icônes des sorts Q/W/E/R.
* **`getChampSkinImg(champ, chemin, version)`** : Télécharge les splash arts de tous les skins du champion.
* **`getChampIcone(version)`** : Récupère toutes les images associées aux champions pour une version (main, passif, sorts, skins).
* **`getAllChampData()` / `getAllChampIcone()` / `getAllChamp()`** : Boucle sur toutes les versions pour récupérer et traiter toutes les données liées aux champions.

### 🛒 Fonctions liées aux objets

* **`getItemImg(version)`** : Télécharge toutes les icônes des objets pour une version donnée.
* **`getItemAllImg()`** : Boucle sur toutes les versions pour récupérer les images de tous les objets.


## 📊 Exemple de table : `champion`

```sql
CREATE TABLE champ_skin (
-- Définition de la clé primaire
	id SERIAL PRIMARY KEY,
	ver_name VARCHAR(100) NOT NULL REFERENCES version(ver_name),
	name VARCHAR(150) NOT NULL,
	champ_name VARCHAR(100),
	skin BYTEA NOT NULL
-- Fin de la déclaration de la table
);
```

## ✨ Améliorations possibles

* Ajouter le support de l'import des **runes**, **sorts d'invocateur** et **cartes**
* Proposer une interface CLI ou web pour piloter les scripts
* Amélioration du template de table qui est catastrophique
* Sécuriser les identifiants via des variables d'environnement
* Rendre le projet compatible avec d'autre SGBD

## 📢 Crédit

Projet développé par Charles Lindecker 2024 (Ce projet à été premier en Python, soyer indulgeant <3) 

* 📧 [charles.lindecker@gmail.com](mailto:charles.lindecker@outlook.com)
* 👤 [LinkedIn](https://www.linkedin.com/in/charleslindecker)
* 💻 [GitHub](https://github.com/Shirou-Emiya2420)

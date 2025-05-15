-- Création de la table version
CREATE TABLE version (
-- Définition de la clé primaire
	id SERIAL PRIMARY KEY, -- Identifiant unique
-- Définition de la clé primaire
	ver_name VARCHAR(100) PRIMARY KEY
-- Fin de la déclaration de la table
);

-- Création de la table global
CREATE TABLE global (
-- Définition de la clé primaire
	id SERIAL PRIMARY KEY,
	ver_name VARCHAR(100) NOT NULL REFERENCES version(ver_name),
	name VARCHAR(50),
	json_data JSONB NOT NULL
-- Fin de la déclaration de la table
);

-- Création de la table champ
CREATE TABLE champ (
-- Définition de la clé primaire
	id SERIAL PRIMARY KEY,
	ver_name VARCHAR(100) NOT NULL REFERENCES version(ver_name),
	champ_name VARCHAR(100),
	main BYTEA NOT NULL,
	passive BYTEA NOT NULL,
	qspell BYTEA NOT NULL,
	wspell BYTEA NOT NULL,
	espell BYTEA NOT NULL,
	rspell BYTEA NOT NULL,
	json_data JSONB NOT NULL
-- Fin de la déclaration de la table
); 

-- Création de la table champ_skin
CREATE TABLE champ_skin (
-- Définition de la clé primaire
	id SERIAL PRIMARY KEY,
	ver_name VARCHAR(100) NOT NULL REFERENCES version(ver_name),
	name VARCHAR(150) NOT NULL,
	champ_name VARCHAR(100),
	skin BYTEA NOT NULL
-- Fin de la déclaration de la table
);

-- Création de la table item
CREATE TABLE item (
-- Définition de la clé primaire
	id SERIAL PRIMARY KEY,
	ver_name VARCHAR(100) NOT NULL REFERENCES version(ver_name),
	name VARCHAR(300),
	json_data JSONB NOT NULL,
	image BYTEA NOT NULL
-- Fin de la déclaration de la table
);

/* Honnêtement la strcture est très mauvaise, je vous invite à ne pas l'utiliser et juste réadapter les put pour votre bdd */
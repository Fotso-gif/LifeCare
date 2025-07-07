-- Création des tables pour la base Lifecare

-- Table des utilisateurs
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(200) NOT NULL,
    status VARCHAR(20) NOT NULL
);

-- Table des maladies
CREATE TABLE maladies (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    soin TEXT NOT NULL
);

-- Table de relation entre utilisateurs et maladies
CREATE TABLE user_maladie (
    user_id INTEGER NOT NULL,
    maladie_id INTEGER NOT NULL,
    PRIMARY KEY (user_id, maladie_id),
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    FOREIGN KEY (maladie_id) REFERENCES maladies (id) ON DELETE CASCADE
);

-- Table des symptômes
CREATE TABLE symptomes (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    categorie VARCHAR(50) NOT NULL
);

-- Table de relation entre maladies et symptômes
CREATE TABLE maladie_symptome (
    maladie_id INTEGER NOT NULL,
    symptome_id INTEGER NOT NULL,
    PRIMARY KEY (maladie_id, symptome_id),
    FOREIGN KEY (maladie_id) REFERENCES maladies (id) ON DELETE CASCADE,
    FOREIGN KEY (symptome_id) REFERENCES symptomes (id) ON DELETE CASCADE
);

-- Table des galleries
CREATE TABLE galleries (
    id SERIAL PRIMARY KEY,
    id_maladie INTEGER NOT NULL,
    image VARCHAR(255) NOT NULL,
    FOREIGN KEY (id_maladie) REFERENCES maladies (id) ON DELETE CASCADE
);

-- Insertion des maladies
INSERT INTO maladies (nom, description, soin) VALUES
('Diabète de type 1', 'Maladie auto-immune qui détruit les cellules bêta du pancréas.', 'Injection d''insuline, suivi médical.'),
('Diabète de type 2', 'Résistance à l''insuline, souvent liée à l''obésité ou au mode de vie.', 'Régime alimentaire, exercice, médicaments.'),
('Cancer du poumon', 'Croissance incontrôlée de cellules dans les poumons.', 'Chimiothérapie, radiothérapie, chirurgie.'),
('Cancer du foie', 'Cancer primaire du foie souvent lié à l''hépatite ou à la cirrhose.', 'Ablation, chimiothérapie ciblée.'),
('Cancer du sein', 'Tumeur maligne développée à partir des cellules du sein.', 'Chirurgie, chimiothérapie, hormonothérapie.');

-- Insertion de quelques symptômes
INSERT INTO symptomes (nom, description, categorie) VALUES
('Fatigue intense', 'Sensation de fatigue persistante même après le repos.', 'general'),
('Soif excessive', 'Besoin constant de boire de l''eau.', 'general'),
('Perte de poids inexpliquée', 'Réduction du poids corporel sans régime ou effort particulier.', 'general'),
('Toux persistante', 'Toux qui dure plus de trois semaines.', 'respiratoire'),
('Douleur thoracique', 'Douleur ou gêne dans la poitrine.', 'respiratoire'),
('Jaunisse', 'Coloration jaune de la peau et des yeux.', 'digestif'),
('Douleur abdominale', 'Douleur dans la région du ventre.', 'digestif'),
('Masse palpable', 'Présence d''une boule ou masse anormale.', 'general');

-- Association des symptômes aux maladies
INSERT INTO maladie_symptome (maladie_id, symptome_id) VALUES
(1, 1), (1, 2), (1, 3),  -- Diabète type 1
(2, 1), (2, 2), (2, 3),  -- Diabète type 2
(3, 1), (3, 4), (3, 5),  -- Cancer poumon
(4, 1), (4, 6), (4, 7),  -- Cancer foie
(5, 1), (5, 3), (5, 8);  -- Cancer sein

-- Insertion de la galleries d'image
INSERT INTO galleries  (id_maladie, image) VALUES
('1','DT1.jpg'),
('1','DT1.1.jpg'),
('1','DT1.2.jpg'),
('1','DT1.3.jpg'),
('1','DT1.4.jpg'),
('1','DT1.5.jpg'),
('1','DT1.6.jpg'),
('1','DT1.7.jpg'),
('1','DT1.8.jpg'),
('1','DT1.9.jpg'),
('1','DT1.10.jpg'),
('2','DT2.jpg'),
('2','DT2.1.jpg'),
('2','DT2.2.jpg'),
('3','CP1.jpg'),
('3','CP2.jpg'),
('3','CP3.jpg'),
('3','CP4.jpg'),
('3','CP5.jpg'),
('4','CF1.jpg'),
('4','CF2.jpg'),
('4','CF3.jpg'),
('5','CS1.jpg'),
('5','CS2.jpg');
-- Création d'un utilisateur admin par défaut
INSERT INTO users (username, email, password_hash, status) VALUES
('admin', 'admin@gmail.com', 'pbkdf2:sha256:260000$Xvx6xVQk5ZQ5J5J5$3e4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d8e7f6', 'admin');
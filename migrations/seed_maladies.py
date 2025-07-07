from app import db
from app.models import Maladie

# Création des objets maladie
maladies = [
    Maladie(nom="Diabète de type 1", description="Maladie auto-immune qui détruit les cellules bêta du pancréas.", soin="Injection d'insuline, suivi médical."),
    Maladie(nom="Diabète de type 2", description="Résistance à l'insuline, souvent liée à l'obésité ou au mode de vie.", soin="Régime alimentaire, exercice, médicaments."),
    Maladie(nom="Cancer du poumon", description="Croissance incontrôlée de cellules dans les poumons.", soin="Chimiothérapie, radiothérapie, chirurgie."),
    Maladie(nom="Cancer du foie", description="Cancer primaire du foie souvent lié à l'hépatite ou à la cirrhose.", soin="Ablation, chimiothérapie ciblée."),
    Maladie(nom="Cancer du sein", description="Tumeur maligne développée à partir des cellules du sein.", soin="Chirurgie, chimiothérapie, hormonothérapie.")
]

# Insertion dans la base de données
db.session.bulk_save_objects(maladies)
db.session.commit()

print("✅ 5 maladies ajoutées avec succès.")

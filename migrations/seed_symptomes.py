from app import app, db
from app.models import Symptome

with app.app_context():
    symptomes = [
        Symptome(nom="Fièvre", description="Température corporelle élevée.", categorie="général"),
        Symptome(nom="Toux", description="Réflexe de défense des voies respiratoires.", categorie="respiratoire"),
        Symptome(nom="Douleurs thoraciques", description="Sensation douloureuse dans la poitrine.", categorie="respiratoire"),
        Symptome(nom="Fatigue chronique", description="Épuisement constant, non soulagé par le repos.", categorie="général"),
        Symptome(nom="Nausées", description="Sensation de vomissement.", categorie="digestif")
    ]
    db.session.bulk_save_objects(symptomes)
    db.session.commit()
    print("✅ Symptômes insérés.")

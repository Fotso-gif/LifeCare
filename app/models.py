from . import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import enum

class UserStatus(enum.Enum):
    admin = "admin"
    patient = "patient"
    docteur = "docteur"
    infirmiere = "infirmiere"

user_maladie = db.Table(
    'user_maladie',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('maladie_id', db.Integer, db.ForeignKey('maladies.id'), primary_key=True)
)

maladie_symptome = db.Table(
    'maladie_symptome',
    db.Column('maladie_id', db.Integer, db.ForeignKey('maladies.id'), primary_key=True),
    db.Column('symptome_id', db.Integer, db.ForeignKey('symptomes.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    status = db.Column(db.Enum(UserStatus), default=UserStatus.patient, nullable=False)
    maladies = db.relationship('Maladie', secondary=user_maladie, back_populates='users')
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.username,
            "email": self.email,
            "status": self.status.value,
            "maladies": [maladie.to_dict() for maladie in self.maladies]
        }
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"
    
class Maladie(db.Model):
    __tablename__ = 'maladies'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    soin = db.Column(db.Text, nullable=False)

    users = db.relationship('User', secondary=user_maladie, back_populates='maladies')
    galleries = db.relationship('Gallery', backref='maladie', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "nom": self.nom,
            "description": self.description,
            "soin": self.soin,
            "galleries": [gallery.image for gallery in self.galleries]
        }
    def __repr__(self):
        return f"<Maladie {self.nom}>"
    


class Symptome(db.Model):
    __tablename__ = 'symptomes'

    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    categorie = db.Column(db.String(50), nullable=False)  # Peut être 'general', 'respiratoire', etc.

    def to_dict(self):
        return {
            "id": self.id,
            "nom": self.nom,
            "description": self.description,
            "categorie": self.categorie
        }
    def __repr__(self):
        return f"<Symptome {self.nom}>"

class Gallery(db.Model):
    __tablename__ = 'galleries'

    id = db.Column(db.Integer, primary_key=True)
    id_maladie = db.Column(db.Integer, db.ForeignKey('maladies.id'), nullable=False)
    image = db.Column(db.String(255), nullable=False)  # chemin ou nom du fichier image

    def to_dict(self):
        return {
            "id": self.id,
            "id_maladie": self.id_maladie,
            "image": self.image
        }
    def __repr__(self):
        return f"<Gallery for Maladie ID {self.id_maladie}>"
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

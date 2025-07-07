from flask_wtf import FlaskForm
#from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import PasswordField, StringField, TextAreaField, SelectField, SelectMultipleField, SubmitField
#from wtforms.validators import DataRequired
class RegisterForm(FlaskForm):
    username = StringField('Nom utilisateur', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    confirm = PasswordField('Confirmer', validators=[EqualTo('password')])
    status = SelectField('Rôle', choices=[('patient', 'Patient'), ('docteur', 'Docteur'), ('infirmiere', 'Infirmière')])
    submit = SubmitField("S'inscrire")

class SymptomForm(FlaskForm):
    age = StringField('Âge', validators=[DataRequired()])
    gender = SelectField('Sexe', choices=[
        ('', 'Sélectionner...'),
        ('male', 'Masculin'),
        ('female', 'Féminin'),
        ('other', 'Autre')
    ], validators=[DataRequired()])
    symptoms = SelectMultipleField('Symptômes', choices=[], coerce=int)  # Les choix seront remplis dynamiquement
    symptom_duration = SelectField('Durée des symptômes', choices=[
        ('', 'Sélectionner...'),
        ('less_than_day', 'Moins d\'un jour'),
        ('1-3_days', '1-3 jours'),
        ('4-7_days', '4-7 jours'),
        ('more_than_week', 'Plus d\'une semaine')
    ])
    additional_info = TextAreaField('Informations complémentaires')
    submit = SubmitField('Obtenir un diagnostic')
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    submit = SubmitField('Connexion')

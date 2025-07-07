import os
from flask import Blueprint, render_template, jsonify, redirect, url_for, flash, request,current_app
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from .forms import RegisterForm, LoginForm, SymptomForm
from collections import defaultdict
from .models import db, Symptome, Maladie, User, UserStatus
from datetime import datetime

main = Blueprint('main', __name__)


#Gestion de la formation des link 
@main.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        maladie_name = request.form['maladie_name']
        image = request.files['image']

        if image:
            # Sécurise le nom du fichier
            filename = secure_filename(image.filename)

            # Crée le dossier spécifique à la maladie
            maladie_folder = os.path.join(current_app.config.get('UPLOAD_FOLDER'), f"maladie_{maladie_name}")
            os.makedirs(maladie_folder, exist_ok=True)

            # Chemin complet du fichier
            filepath = os.path.join(maladie_folder, filename)

            # Sauvegarde sur le disque
            image.save(filepath)

            # Enregistrer dans la BD (exemple)
            chemin_relatif = filepath  # Ou os.path.relpath(filepath)
            # Exemple : Maladie(nom=maladie_name, image_path=chemin_relatif)

            return f"Image enregistrée à {filepath}"

    return jsonify({
        'success': True,
            'data': chemin_relatif,
            'count': len(chemin_relatif)
        })

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            status=UserStatus[form.status.data]
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Inscription réussie.')
        return redirect(url_for('main.login'))
    return render_template('auth/register.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        flash('Identifiants invalides.')
    return render_template('auth/login.html', form=form)



@main.route('/dashboard')
@login_required
def dashboard():
    user_data = {
        'username': current_user.username,
        'email': current_user.email,
        'status': current_user.status.value,
        'avatar': current_user.username[0].upper()  # Première lettre pour l'avatar
    }
    date_du_jour = datetime.now().strftime("%d/%m/%Y")
    
    if current_user.status.value in ['admin', 'docteur']:
        maladies = Maladie.query.all()
        data = [maladie.to_dict() for maladie in maladies]  # Convertir les objets Maladie en dictionnaires
        
        # Convertir les objets Produit en dictionnaires
        
        return render_template('back/espace_client.html', 
                        success = True,     
                            user = user_data,
                            date_du_jour = date_du_jour,
                            is_admin = True,
                            maladies = data
                        )
    else:
        user_maladies = current_user.maladies
        return render_template('back/espace_client.html', 
                        success = False, 
                            user = user_data,
                            date_du_jour = date_du_jour,
                            is_admin = False,
                            maladies = data
                        )
@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main.route('/')
def index():
    user = current_user
    if not user.is_authenticated:
        
        #flash('Vous devez être connecté pour accéder à votre profil.', 'warning')
        return render_template('front/index.html',
            message = 'Vous devez vous connecter.', 
            is_connect = False
            )
    return render_template('front/index.html',message = 'vous etes connectes',is_connect = True)

@main.route('/diagnostic', methods=['GET', 'POST'])
def diagnostic():
    form = SymptomForm()
    
    # Remplir dynamiquement les choix de symptômes depuis la base de données
    form.symptoms.choices = [(s.id, s.nom) for s in Symptome.query.order_by('nom')]
    
    def diagnose(selected_symptoms):
        """Fonction de diagnostic simplifiée qui trouve les maladies correspondantes"""
        # Créer un dictionnaire pour compter les correspondances
        maladie_scores = defaultdict(int)
        
        # Pour chaque maladie, vérifier combien de symptômes correspondent
        for maladie in Maladie.query.all():
            for symptom in selected_symptoms:
                if symptom.nom.lower() in maladie.description.lower():
                    maladie_scores[maladie] += 1
        
        # Trier les maladies par score décroissant
        sorted_maladies = sorted(maladie_scores.items(),
                                key=lambda x: x[1],
                                reverse=True)
        
        # Ne retourner que les maladies avec au moins un symptôme correspondant
        return [m for m, score in sorted_maladies if score > 0]

    if request.method == 'POST' and form.validate_on_submit():
        try:
            # Récupérer les données du formulaire
            age = form.age.data
            gender = form.gender.data
            symptom_ids = form.symptoms.data
            duration = form.symptom_duration.data
            additional_info = form.additional_info.data
            
            # Récupérer les objets Symptome complets
            selected_symptoms = Symptome.query.filter(Symptome.id.in_(symptom_ids)).all()
            
            # Logique de diagnostic (simplifiée)
            possible_maladies = diagnose(selected_symptoms)
            
            # Préparer les données pour le template
            symptom_names = [s.nom for s in selected_symptoms]
            
            user_data = {
                'username': current_user.username,
                'email': current_user.email,
                'status': current_user.status.value,
                'avatar': current_user.username[0].upper()  # Première lettre pour l'avatar
            }
            
            
            return jsonify({
                                'age':age,
                                # 'user':user_data,
                                'gender':gender,
                                'symptoms':symptom_names,
                                'duration':duration,
                                'additional_info':additional_info,
                                'possible_maladies':possible_maladies})
            
        except Exception as e:
            flash('Une erreur est survenue lors du diagnostic: ' + str(e), 'danger')
            return redirect(url_for('diagnostic'))
    
    return jsonify({ 
                    'message':'Entrer vos données via le curl',
                    # 'form':form,
                    # 'user':user_data
                    })

    
#Teste de connexion a la base de données
@main.route('/test-db')
def test_db():
    try:
        db.session.execute('SELECT 1')
        return "Connexion à PostgreSQL fonctionnelle!"
    except Exception as e:
        return f"Erreur de connexion: {str(e)}", 500

@main.route('/profile')
def profile():
    user_data = {
        'username': current_user.username,
        'email': current_user.email,
        'status': current_user.status.value,
        'avatar': current_user.username[0].upper()  # Première lettre pour l'avatar
    }
    if not current_user.is_authenticated:
        flash('Vous devez être connecté pour accéder à votre profil.', 'warning')
        return redirect(url_for('main.login'))
    return render_template('back/profile.html',
                    user = user_data
                )
@main.route('/profile/edit', methods=['GET', 'POST'])
def edit_profile():
    user = current_user
    user_data = {
        'username': current_user.username,
        'email': current_user.email,
        'status': current_user.status.value,
        'avatar': current_user.username[0].upper()  # Première lettre pour l'avatar
    }
    if not user.is_authenticated:
        flash('Vous devez être connecté pour modifier votre profil.', 'warning')
        return redirect(url_for('main.login'))
    
    if request.method == 'POST':
        user.username = request.form.get('username', user.username)
        user.email = request.form.get('email', user.email)
        db.session.commit()
        flash('Profil mis à jour avec succès.', 'success')
        return redirect(url_for('main.dashboard'))
    
    return render_template('back/profile.html',user = user_data)

#Gestion des maladies
@main.route('/maladies')
@login_required
def gestion_maladies():
    if current_user.status.value not in ['admin', 'docteur']:
        flash('Accès non autorisé', 'danger')
        return redirect(url_for('main.dashboard'))
    user = current_user
    
    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    # Récupération des maladies avec pagination
    maladies = Maladie.query.order_by(Maladie.nom.asc()).paginate(page=page, per_page=per_page)
    
     # Sérialisation des données
    maladies_data = [{
        'id': maladie.id,
        'nom': maladie.nom,
        'description': maladie.description
        # Ajouter d'autres champs nécessaires
    } for maladie in maladies.items]
    # Réponse JSON sécurisée
    return jsonify({
        'maladies': maladies_data,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total_pages': maladies.pages,
            'total_items': maladies.total
        },
        'user_info': {
            'id': current_user.id,
            'role': current_user.status.value
            # Ne pas exposer d'autres infos sensibles
        }
    })

@main.route('/maladie/<int:maladie_id>')
@login_required
def voir_maladie(maladie_id):
    maladie = Maladie.query.get_or_404(maladie_id)
    maladie_data = maladie.to_dict() 
    user_data = {
        'username': current_user.username,
        'email': current_user.email,
        'status': current_user.status.value,
        'avatar': current_user.username[0].upper()  # Première lettre pour l'avatar
    }
    return jsonify({ 'user':user_data,'maladie':maladie_data})

@main.route('/maladie/ajouter', methods=['GET', 'POST'])
@login_required
def ajouter_maladie():
    if current_user.status.value not in ['admin', 'docteur']:
        flash('Accès non autorisé', 'danger')
        return redirect(url_for('main.dashboard'))
    
    if request.method == 'POST':
        nom = request.form.get('nom')
        description = request.form.get('description')
        soin = request.form.get('soin')
        if nom and description and soin:
            ml = Maladie(nom=nom, description=description, soin=soin)
            db.session.add(ml)
            db.session.commit()
            flash('Maladie ajoutée avec succès', 'success')
            return redirect(url_for('main.voir_maladie', maladie_id=ml.id))
        else:
            flash('Veuillez remplir tous les champs', 'danger')
            return redirect(url_for('main.ajouter_maladie'))
    
    symptomes = Symptome.query.all()
    symptome_data = [ symptome for symptome in symptomes]
    return jsonify({'symptomes':symptome_data})

@main.route('/maladie/supprimer/<int:maladie_id>', methods=['POST'])
@login_required
def supprimer_maladie(maladie_id):
    if current_user.status.value not in ['admin', 'docteur']:
        flash('Accès non autorisé', 'danger')
        return redirect(url_for('main.dashboard'))
    
    maladie = Maladie.query.get_or_404(maladie_id)
    db.session.delete(maladie)
    db.session.commit()
    flash('Maladie supprimée avec succès', 'success')
    return redirect(url_for('main.gestion_maladies'))
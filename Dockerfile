# Utilisez une image Python officielle comme base
FROM python:3.9-slim

# Définissez le répertoire de travail
WORKDIR /app

# Copiez les fichiers requis
COPY requirements.txt .

# Installez les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copiez le reste des fichiers
COPY . .

# Exposez le port utilisé par Flask (généralement 5000)
EXPOSE 5000

# Commande pour lancer l'application
CMD ["python", "run.py"]
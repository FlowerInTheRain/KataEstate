# Utiliser l'image officielle de PostgreSQL 15
FROM postgres:15

# Définir des variables d'environnement pour configurer PostgreSQL
ENV POSTGRES_USER=kata
ENV POSTGRES_PASSWORD=kataaubay
ENV POSTGRES_DB=kata

# Copier le fichier d'initialisation SQL dans le répertoire d'initialisation du conteneur
# Ce fichier va être exécuté lors du démarrage du conteneur
COPY init.sql /docker-entrypoint-initdb.d/

# Exposer le port 5432
EXPOSE 5432
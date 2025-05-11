## Property Management Kata - Python

# Environment 
* Windows 11 home
* Python 3.12+
* WSL Ubuntu
* Flask 3.1.0 (API)
* Flask-restx + Marshmallow (API Documentation)
* SQLAlchemy 2.0
* Pycharm

## Commandes docker

A executer dans le répertoire du docker-compose.yaml

```
docker compose up --build
(pour supprimer les containers en cli) => docker rm $(docker ps -a -q)
```
 
# créer venv
python -m venv nom_du_venv

# activer venv
source .venv/bin/activate
(à la racine du projet)

# créer requirements.txt depuis venv
pip freeze > requirements.txt

# executer les tests unitaires
Lancer le venv
PYTHONPATH=app pytest tests/

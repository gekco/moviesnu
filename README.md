# moviesnu

requirements:
 python 3.4,virtualenv,mysql

virtual venv
source venv/bin/activate
pip install -r requirements.pip

UPDATE moviesnu/moviesnu/settings.py(DATABASE)

on mysql:
  create database moviesnu

on bash:
  python manage.py makemigrations
  python manage.py migrate
  python manage.py runserver

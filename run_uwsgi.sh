pip install -r requirements.txt
python manage.py migrate
sh create_superuser.sh
uwsgi --http :8000 --chdir /www/server --module flatcoke.wsgi


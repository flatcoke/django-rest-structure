pip install -r requirements.txt
python manage.py migrate
uwsgi --http :8000 --chdir /www/server --module flatcoke.wsgi


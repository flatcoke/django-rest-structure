FROM python:3.6

ENV PYTHONUNBUFFERED 1
RUN mkdir -p /www/server
WORKDIR /www/server

# this section is very important to keep a separate layer for the dependencies
ADD . /www/server/
# RUN virtualenv -p python3 env
# RUN source env/bin/activate
RUN pip install -r requirements.txt

# build static assets
RUN python manage.py collectstatic -v 0 --clear --noinput

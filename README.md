## Stack
* python 3.6
* django 2.1
* restframework 3.9
* celery 4.2 (Redis queue)
* life-cycle (Helper for model signal(hook))
* swagger
* JWT


### Evironment
```console
$ cp .env_example .env
```

### Run
```console
$ docker-compose up
```
* Needs to take time on first up


## Test
```console
$ docker-compose exec -it app python manage.py test
```

## URL
[http://localhost:8000/doc (login page and redirect)](http://localhost:8000/login/?next=/doc/)

* email: `admin@example.com` password: `qwer1234`

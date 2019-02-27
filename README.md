## Stack
* **python** 3.6
* **django** 2.1
* **restframework** 3.9
* **celery** 4.2: job Worker with Redis queue
* **life-cycle**:  Helper for model signal(hook)
* **django-cacheops**: django ORM cache
* **swagger**: api documentation
* **JWT**: authority
* **etc** ~


### Evironment
```console
$ cp .env_example .env
```

### Run
```console
$ docker-compose up
```

## Test
```console
$ docker-compose exec -it app python manage.py test
```

## URL
[http://localhost:8000/doc (Click here)](http://localhost:8000/login/?next=/doc/)

* email: `admin@example.com` password: `qwer1234`

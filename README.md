## Stack
* **python** 3.6
* **django** 2.1
* **restframework** 3.9
* **celery** 4.2: job Worker with Redis queue and Flower monitoring tool
* **life-cycle**:  Helper for model signal(hook)
* **django-cacheops**: django ORM cache
* **swagger**: api documentation
* **JWT**: authentication
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
[http://localhost:8000/doc](http://localhost:8000/login/?next=/doc/) Documentation(swagger)
* **email**: `admin@example.com` **password**: `qwer1234`

[http://localhost:8888](http://localhost:8888) Job monitor(flower)

# recipe-app-api



# Running in docker flake8:

```bash
 docker compose run --rm app sh -c "flake8"
 ```


## Create Django App

```bash
docker compose run --rm app sh -c "django-admin startproject  app ."
```


Ruunning the tests in docker:

```bash
docker compose run --rm app sh -c "python manage.py test"
```



# create a application in docker:

```bash
docker compose run --rm app sh -c "python manage.py startapp core"
```


# Testing the wait_for_db command and the flake8 command in docker:

```bash
 docker compose run --rm app sh -c "python manage.py test && flake8"
```

```bash
docker compose run --rm app sh -c "sleep 5 && python manage.py test"
```


```bash
docker compose run --rm app sh -c "python manage.py wait_for_db && flake8"
```



 Wipe volume and restart clean:
```bash
docker compose down -v
docker compose up --build
```


add user to project:

```bash
docker compose run --rm app sh -c "python manage.py makemigrations"
```

then migrate the database:

```bash
docker compose run --rm app sh -c "python manage.py migrate"
```


# how to remove a database in docker:

1. check all of volume in docker:

```bash
docker volume ls
```

2. remove the database volume:
```bash
docker volume rm <volume_name>
```

3. if docker volume rm <volume_name> does not work, then remove the volume with force:
3. docker compose down

```bash
docker compose down
```

then remove the volume with force:
```bash
docker volume rm <volume_name>
```



How to create a superuser admin in docker:

```bash
docker compose run --rm app sh -c "python manage.py createsuperuser"
```

admin: admin@exmaple.com
password: admin123


# How to create an application in docker:

```bash
docker compose run --rm app sh -c "python manage.py startapp <app_name>"
```

example:
```bash
docker compose run --rm app sh -c "python manage.py startapp user"
```


```docs
http://127.0.0.1:8000/api/docs
```

```admin
http://127.0.0.1:8000/admin
```


# Github Repository:

https://github.com/alinemati-uwm/recipe_app_api

Django best Practice model:

https://github.com/vahidrnaderi/django-project-structure

```bash
project_root/
├── deployments/                # Isolate Dockerfiles and docker-compose files here.
│   ├── Dockerfile
│   ├── Dockerfile_dev
│   ├── Dockerfile_prod
│   └── docker-compose.yml
├── docs/
│   ├── CHANGELOG.md
│   ├── CONTRIBUTING.md
│   ├── deployment.md
│   ├── local-development.md
│   └── schema.yml
├── local_db/
├── locale/
├── logs/
├── media/
├── project_name/
│   ├── apps/
│   │   ├── app1/               # A django rest app
│   │   │   ├── api/
│   │   │   │   ├── v1/         # Only the "presentation" layer exists here.
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── serializers.py
│   │   │   │   │   ├── urls.py
│   │   │   │   │   └── views.py
│   │   │   │   ├── v2/         # Only the "presentation" layer exists here.
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   ├── serializers.py
│   │   │   │   │   ├── urls.py
│   │   │   │   │   └── views.py
│   │   │   │   └── __init__.py
│   │   │   ├── fixtures/       # Constant "seeders" to populate your database
│   │   │   ├── management/
│   │   │   │   ├── commands/   # Try and write some database seeders here
│   │   │   │   │   ├── __init__.py
│   │   │   │   │   └── command.py
│   │   │   │   └── __init__.py
│   │   │   ├── migrations/
│   │   │   │   └── __init__.py
│   │   │   ├── templates/      # App-specific templates go here
│   │   │   ├── tests/          # All your integration and unit tests for an app go here.
│   │   │   │   ├── __init__.py
│   │   │   │   └── test_app1_name.py
│   │   │   ├── __init__.py
│   │   │   ├── admin.py
│   │   │   ├── apps.py
│   │   │   ├── models.py
│   │   │   ├── services.py     # Your business logic and data abstractions go here.
│   │   │   ├── urls.py
│   │   │   └── views.py
│   │   ├── app2/               # A django rest app same as app1 structure
│   │   └── core/               # A django rest core same as app1 structure plus following files
│   │       ├── constants.py
│   │       ├── exceptopns.py
│   │       └── helpers.py
│   ├── common/                 # An optional folder containing common "stuff" for the entire project
│   │   ├── __init__.py
│   │   ├── common.py
│   │   ├── constants.py
│   │   ├── generics.py
│   │   ├── helpers.py
│   │   ├── mixins.py
│   │   ├── models.py
│   │   └── serializers.py
│   └── config/
│       ├── settings
│       │   ├── __init__.py
│       │   ├── development.py
│       │   ├── production.py
│       │   └── staging.py
│       ├── __init__.py
│       ├── asgi.py
│       ├── urls.py
│       └── wsgi.py
├── requirements/
│   ├── common.txt              # Same for all environments
│   ├── development.txt         # Only for a development server
│   ├── local.txt               # Only for a local server (example: docs, performance testing, etc.)
│   ├── production.txt          # Production only
│   └── requirements-dev.txt
│   └── requirements.txt
├── scripts/                    # Your script files
│   └── entrypoint.sh           # Any bootstrapping necessary for your application
├── static/                     # Your static files
│   ├── css/
│   ├── images/
│   └── js/
├── .dockerignore
├── .env
├── .env.example                # An example of your .env configurations. Add necessary comments.
├── .flake8
├── .gitignore                  # https://github.com/github/gitignore/blob/main/Python.gitignore
├── LICENSE
├── manage.py
├── Pipfile
├── Pipfile.lock
├── pyproject.toml
├── pytest.ini
├── README.md
├── setup.cfg
├── setup.py
└── tox.ini
```

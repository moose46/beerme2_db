# Beer Me with Database

## Replacement for beer me

### code

### create env 3.12.3

### Install Django

``` cmd
 python -m pip install Django==5.1.6
```

### Start Project from VisualCode

### <https://docs.djangoproject.com/en/5.1/intro/tutorial01/>

```
mkdir beerme2_db
django-admin startproject beer beerme2_db
python manage.py startapp commissioner
pip install mssql-django
```

### to run program

```
python manage.py runserver
```

### to load race results

```
python manage.py runscript load_race_results
```

### Database Information

---

#### pgadmin4 PostgresSQL 16 password:admin

#### database:beer_me user:bob password: admin role:bob

#### python manage.py runscript copy_race_data --script-args 2025
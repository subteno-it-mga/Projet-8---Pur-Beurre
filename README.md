# Projet-8---Pur-Beurre For Open Class Room
## This project is made for the OpenClassRoom course (DA PYTHON)

## What is this project and how it works ?
This application retrieve products from the OpenFoodFact API. We store it in database. Then, we can compare products
and add subsitutes in favorite in your personnal space.

## To install the project on your pc, please follow these instructions:

### 1 - Fork the project

### 2 - Clone the project on your PC

### 3 - Create and set the database
In this case i use postgresql, but we can use an other db engine.

**STEP 1 :** 
Create a database.

```sql
createdb <your database name>
```

**STEP 2:**
Create your virtualenv in this path: Projet OpenClassRoom/Projet-8-Pur-Beurre.

```bash
virtualenv env -p python3
```

**STEP 3 :** 
Setting up the database in PurBeurre/settings.py

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '<your database name>',
        'USER': '<your username>',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '5432',
    }
}
```

**STEP 4 :**
Migrate the model into the database

*you must be at this location to launch the command: Projet OpenClassRoom/Projet-8-Pur-Beurre/PurBeurre*

```bash
./manage.py migrate
```

**STEP 5 :**
Launch the server with the following command

```python
./manage.py runserver
```

Then go to localhost: http://127.0.0.1:8000/

Search a product in the input field and have fun :)

### BONUS - Basic commands to run the project


#### Migrate data models

```python
./manage.py showmigrations
./manage.py makemigrations
```

#### Launch tests

It will launch the test to check if the project is still viable or has errors.

```python
./manage.py test search_food
```

#### Check the test coverage

This show the coverage of the code.

```python
coverage run --source='.' manage.py test search_food
coverage report
```



This project was made by Martin Gaucher for Open Class Room.



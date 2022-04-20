# Corporate Address Manager

A Company Address manager Book built on django

## Pre-requisites
* Python

### Installing

1. install all the packages and dependencies by the following command:
```
pip install -r requirements.txt

```
2. Before running the application, create a mysql database on your localhost and update the database configuration on the settings.py file or create a demo database according to the built in configuration below.

```
Database name: 'CAmanager',
USER: 'test',
PASSWORD: 'Secret_1234'
HOST    : 'localhost'
```

3. Run the following commands:

```
python manage.py makemigrations
```

```
python manage.py migrate
```

4. Run the server

```
python manage.py runserver
```

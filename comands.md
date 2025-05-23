# multiple users and databases restfull api


## start up and enviorement instalation
we start by downloading the template from here
```
https://github.com/bugbytes-io/Django-HTMX-Finance-App.git
```
in that link we had
- project name = finance_project
- tracker = name of the app
- static = we add the static values here

yo create an enviroment we use this command
```
python -m venv NAME_ENVIROMENT
```

activate that enviroment
```
NAME_ENVIROMENT\Scripts\activate
```

install the requiriments
```
pip install -r requirements.txt
```

================================
## install projects and apps

this its how we install the project
```
django-admin startproject NAMEPROJECT .
```

this its how we instal the apps
```
python manage.py startapp NAMEAPP
```

================================
## postgres 

postgress details
```
name = Myserver
hostname = localhost
user = postgres
pass = 1234
port = 5432
```

to start a session in postgress we use
```
psql -U postgres
```

create a database
```
CREATE DATABASE NAME_DATABASE_HERE OWNER postgres;
```

name of the databases for this project
```
db_listing
db_user
```

commands inside postgres
```
#list of the tables of the database
\dt


# when querying dont forget to use ; at the end
SELECT * from TABLENAME;
```
================================
## migrate django
<!-- ---- preparing the migration -->
to make and prepare the model to be migrated
```
python manage.py makemigrations
```

migrate the database
```
python manage.py migrate

# migrate to an specific app and database
python manage.py migrate NAMEAPP --database=NAMEDATABASE_DESTINY

# but also we could migrate all the database include the admin tables like this
python manage.py migrate --database=NAMEDATABASE_DESTINY
```
python manage.py migrate --database=users_db

create a super user to connect to admin
```
python manage.py createsuperuser

#to store the values in a specific database we use
# --database=NAMEDATABASE <==== eso tiene que estar todo junto
python manage.py createsuperuser --database=NAMEDATABASE
```

serttings of the superuser
```
user = bis@bis.com 
name = hs
password = 123
```

# ==============================
# ==============================
# ==============================

# Deploy GIT

do this in local
```
git init
git add .
git commit -m "first commmit"
```
for the next step we need the git link avaiable or created
we paste this line from git to create the connection
```
git remote add origin https://github.com/auszed/djangoCrud.git
git push origin MASTERORMAIN
```

================================
## run de service
tun the app
```
python manage.py runserver
```

in this app we run the envoriment like this
```
venv\Scripts\activate
```


================================
## create logins auth

create an app for registration for the app
```
python manage.py startapp registration
```
this its the url of it
http://127.0.0.1:8000/accounts/




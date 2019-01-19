###Project name:
Accomendation Web Portal 

###Build:
>Version Control:  
Python3.6
Django 2.1


###Setup
1. git clone git@bitbucket.org:wam849/zeta.git

### FOR MAC USERS (using virtual environment)
1. virtualenv venv
2. source venv/bin/activate

### INITIAL SETUP (only once):
1. create a database in postgresql (name it whatever)
2. update DATABASES parameter in zeta/settings.py accordingly (NAME, PASSWORD, etc)
3. pip install django
4. pip install psycopg2
5. pip install django-bootstrap4
6. python manage.py makemigrations
7. python manage.py migrate
8. python manage.py loaduser
9. python manage.py loaddata listings.json
10. python manage.py loaddata calendars.json
11. python manage.py loaddata reviews.json

### HOW TO RUN:
>python manage.py runserver. 
  
Visit http:// localhost:8000 in browser  
You can decide to use "guest mode" or "log in mode" to use our project

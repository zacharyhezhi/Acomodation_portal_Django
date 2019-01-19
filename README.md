Project name:</br>
Accomendation Web Portal

Build:</br>
Version Control:</br>
Python3.6 Django 2.1 </br>
Setup</br>
git clone git@bitbucket.org:wam849/zeta.git</br>
FOR MAC USERS (using virtual environment)</br>
virtualenv venv</br>
source venv/bin/activate</br>
INITIAL SETUP (only once):</br>
create a database in postgresql (name it whatever)</br>
update DATABASES parameter in zeta/settings.py accordingly (NAME, PASSWORD, etc)</br>
pip install django</br>
pip install psycopg2</br>
pip install django-bootstrap4</br>
python manage.py makemigrations</br>
python manage.py migrate</br>
python manage.py loaduser</br>
python manage.py loaddata listings.json</br>
python manage.py loaddata calendars.json</br>
python manage.py loaddata reviews.json</br>
HOW TO RUN:</br>
python manage.py runserver.  </br>
Visit http:// localhost:8000 in browser</br>
You can decide to use "guest mode" or "log in mode" to use our project</br>

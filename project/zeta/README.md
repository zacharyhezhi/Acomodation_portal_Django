# ZETA

**ZETA** is a web application that will allow providers to present their property, and visitors to review the offers and reserve or rent a property. Visitors can also create a request if they cannot find a suitable property.

### Django Applications
This project focuses on the creation of a generic, modular architecture for building web portals that can be used for accommodation or other similar services, which will be based on five core components:
- _users/_ : **Custom User Module** - allows users to login using email instead of username.
- _advertising/_ : **Accommodation Advertising Module** - for providers of accommodations to advertise properties and manage their advertisements
- _request/_ : **Visitor Request Module** - for visitors to put their requests and get a simple and useful feedback of the available accommodations, and to select and book preferred accommodation
- _search/_ : **Accommodation Search Module** - for users to find properties and filters out inappropriate ones
- _review/_ : **Accommodation Review Module** - for visitors to publish a review of the properties they have stayed in

### Initial Setup
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

### How to Run
1. python manage.py runserver
2. Navigate to http://localhost:8000/home

### The Team
1. Andrew Wirjaputra (Backend + Frontend integration)
2. Shengtao Xu (Frontend)
3. Shiqing Zhang (Frontend)
4. Zhi He (Frontend)
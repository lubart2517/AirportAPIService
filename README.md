# AirportAPIService
A RESTful API for an airport service
This project should be launched in docker container (use docker-compose up)
It's possible also to launch without docker, use sqlite config of database
from settings.py and python manage.py runserver command

create your ovn .env file according to .env.sample

to create superuser:
python manage.py createsuperuser

to load fixture data:
python manage.py loaddata db_to_load.json

to create user:
api/user/register

to get access and refresh tokens:
api/user/token

All documentation available at api/doc/swagger/






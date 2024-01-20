# AirportAPIService

## Introduction and Overview

A RESTful API for an airport service.
Allow manage Airplanes, Airports, Routes, Crew and so on.

## Installation Instructions
Install PostgreSQL and create a database.
Clone the GitHub repository: 
git clone https://github.com/lubart2517/AirportAPIService.git
Navigate to the project directory: cd AirportAPIService
Create a virtual environment and activate it:
python -m venv .venv
source venv/bin/activate
Install required dependencies: pip install -r requirements.txt
Create your ovn .env file according to .env.sample or set environment 
variables for database connection:
set POSTGRES_HOST=<your db hostname>
set POSTGRES_DB=<your db name>
set POSTGRES_USER=<your db username>
set POSTGRES_PASSWORD=<your db user password>
Set a secret key: set SECRET_KEY=<your secret key>

Run database migrations: python manage.py migrate
Start the development server: python manage.py runserver

This project should be launched in docker container (use docker-compose up)


## Usage Guidelines
To create superuser:
python manage.py createsuperuser

To load fixture data:
python manage.py loaddata db_to_load.json

To create user:
api/user/register

To get access and refresh tokens:
api/user/token

To visit start page, add Authorization header with value:
"Bearer <your access token>" and go to /api/airport/


## Configuration Details
Documentation is located at /api/doc/swagger/: 
This means that the API documentation is located at the URL /api/doc/swagger/


## Features
API is JWT authenticated: 
This means that the admin panel is protected using JSON Web Tokens (JWTs). 
JWTs are a secure way to authenticate users without storing their passwords 
on the server

Key project features
1.	Managing orders and tickets
2.	Creating routes, planes, types, 
3.	Creating airports, receiving airport routes
4.	Adding flights, receiving crew members for each flight
5.	Filtering flights, crews, flight_crew_members

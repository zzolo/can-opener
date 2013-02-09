# Can Opener

A small application to look at the Minneapolis license plate tracking data.  Aimed at creating an intelligent conversation about the data.

## Installation

1. Install ```pip```
1. Install ```virtualenv```
1. Make a virtualenv and enable it.
1. Install requirements: ```pip install -r requirements.txt```
1. Setup postgres database: ```createdb -U postgres -h localhost can_opener````
    * If using PostGIS: ```createdb -U postgres -h localhost -T template_postgis can_opener````
1. Set database connection variable: ```export DATABASE_URL="postgres//postgres:@localhost:5432/can_opener"```
1. Run: ```python dl.py``` (this will take a moment)
1. Run: ```python import.py``` (this will take some time)

## Deployment

Meant for Heroku.

1. ```heroku create app-name```
1. 
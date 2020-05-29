# Agregator

This is a skeleton of Agregator Rest Application.

## Single command build script

The main part of app is `core` application. This app allows us to easily build solution. 
Building script is created based on django framework commands. This means you can build whole app, but also, perform each of the commands. 

There are 5 commands: 

1. buildapp 
2. cleardatabase
3. initializedata
4. pytest_runner
5. removemigrations


### buildapp
Builds entire solution, run tests, `deletes db(!)`. 
To perform building script you need provide single argument: profile.
The building script can be run with one of 3 different profiles:

development, test, production

Running script with production, need PRODUCTION env variable set to true. 

`PRODUCTION` environment does not delete db. 


    python manage.py buildapp --profile development
    

#### cleardatabase
Deletes all tables in Postgres orz MySQl DB, in case of using Sqlite, deletes file.
 
    python manage.py cleardatabase
    
    
#### removemigrations
Deletes all migration files in entire solution. 

    python manage.py removemigrations

#### initializedata
Runs intitialization script, to seed db, and perform any other action. You can easily add functions to initializedata. Consider, that each app should have their own initializedata function, and only those functions should be in script. One App - one line to perform. 
 
    python manage.py initializedata

#### pytest_runner
Runs all pytest tests. 

    python manage.py pytest_runner

## Environment settings

Environment settings can be easily customized in `app_settings.json` file in root of application. 
Consider this should bo only root json, no nested elements allowed.

## Install

    python manage.py buildapp --profile development
    python manage.py ldap_sync_users

## Run the app
App will be run on loopback: 127.0.0.1:8000 - on default port

    python manage.py runserver

## Run the tests

To perform tests with pytest:

    pytest

# REST API

REST APi should be developed based on each application. Root of API is in apa_plot app - `urls.py`
To allows for easily checking, for tests, and better, quicker development we provided Swagger. 

Swagger allows to show all API endpoints in friendly for developers way.

    http://127.0.0.1:8000/swagger/


### Endpoints

#### Request

`POST api/v1/hello-world`
    
    {}

# README #

This README would normally document whatever steps are necessary to get your application up and running.

# DORIS Procurements

DORIS Procurements is an application that assists individuals in the process of submitting procurement requests which are then routed for approval.

# Technical Details
DORIS Procurements is a Python web application built using the Flask framework for the backend. The frontend is built using the Bootstrap framework. Procurements is compatible with most modern browsers, including Internet Explorer 11 and above.

## Setup Instructions
Clone the git repository and make it your current directory:
```bash
git clone git@gitlab.com:nycrecords/doris_procurements.git
cd doris_procurements
```

Make sure you have `postgresql` and `libpq` installed.
Create a virtual environment and install the requirements:
```bash
python3 -m venv procurements
source procurements/bin/activate
pip install -r requirements.txt
```

Initialize the database by entering the following in the psql line:
```bash
psql postgres
username=# create database procurement;
username=# \q
```

Upgrade the database by entering the following in the command line:
```bash
flask db upgrade
```

Locally run the intranet by entering the following in the command line:
```bash
python manage.py runserver
```

## Troubleshooting
### Psycopg2 can't find the dynamic library of `libpq`
For development, the alternative package `psycopg2-binary` can be used to `psycopg2`.
For production, `psycopg2` should be compiled from source.

### Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines

### Who do I talk to? ###

* Repo owner or admin
* Other community or team contact

# README #

This README would normally document whatever steps are necessary to get your application up and running.

# DORIS Procurements

DORIS Procurements is an application that assists individuals in the process of submitting procurement requests which are then routed for approval.

# Technical Details
DORIS Procurements is a Python web application built using the Flask framework for the backend. The frontend is built using the Bootstrap framework. Procurements is compatible with most modern browsers, including Internet Explorer 11 and above.

## Setup Instructions
Clone the git repository and make it your current directory:

    git clone https://mlaikhram@bitbucket.org/nycrecordswebdev/doris_procurements.git
    cd doris_procurements

Run the build scripts:

    sudo sh build_scripts/web_setup/web_setup.sh single_server
    sudo sh build_scripts/app_setup/app_setup.sh single_server
    sudo sh build_scripts/db_setup/db_setup.sh single_server
    sudo sh build_scripts/db_setup/db_user_setup.sh

Upgrade the database by entering the following in the command line:

    python manage.py db upgrade

Add admins to the database by entering the following in the command line:

    python manage.py db create_admin first_name last_name email

Note that each admin should update their profile upon logging in by filling out the required fields and updating the password.

Locally run the intranet by entering the following in the command line:

    python manage.py runserver


### Contribution guidelines ###

* Writing tests
* Code review
* Other guidelines

### Who do I talk to? ###

* Repo owner or admin
* Other community or team contact
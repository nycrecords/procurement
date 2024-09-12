import os
from uuid import uuid4

import click
from flask_migrate import Migrate

from app import create_app, db
from app.constants import division, roles
from app.models import User, Request

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Request=Request)


@app.cli.command()
def list_routes():
    """List all routes in the Flask application."""
    import urllib.parse
    output = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(rule.methods)
        url = urllib.parse.unquote("{:50s} {:20s} {}".format(
            rule.endpoint,
            methods,
            rule
        ))
        output.append(url)

    for line in sorted(output):
        click.echo(line)


@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@app.cli.command()
def assign_admin_role():
    """Assigns the admin role to a specified user based on their email from the command line."""
    user_email = input("Enter user email: ").strip()
    user = User.query.filter_by(email=user_email).first()

    if user is None:
        print("User not found.")

    else:
        # Update user role and division
        user.role = roles.ADMIN
        user.division = division.ADM
        db.session.commit()
        print(f"Successfully assigned admin role to user {user_email}")


@app.cli.command()
def create_test_admin_user():
    """Allows the user to create  a test admin account from the command line"""
    first_name = input("Enter user first name: ").strip()
    last_name = input("Enter user last name: ").strip()
    email = input("Enter user email: ").strip()

    if not (first_name and last_name and email):
        print("First name, last name, and email are required.")
        return

    new_user = User(email=email,
                    division=division.MRMD,
                    first_name=first_name,
                    last_name=last_name,
                    guid=uuid4().hex,
                    phone=None,
                    address=None,
                    role=roles.ADMIN)

    db.session.add(new_user)
    db.session.commit()

    print("Account successfully created!")

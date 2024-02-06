import click
from werkzeug.security import generate_password_hash
import os
from app import create_app, db
from app.models import User, Request
from app.constants import division, roles
from flask_migrate import Migrate

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
def create_admin():
    """Allows the user to create an admin account from the command line"""
    first_name = input("Enter user first name: ")
    last_name = input("Enter user last name: ")
    email = input("Enter user email: ")
    new_user = User(email=email,
                    division=division.MRMD,
                    password_hash=generate_password_hash("Change4me"),
                    first_name=first_name,
                    last_name=last_name,
                    phone=None,
                    address=None,
                    role=roles.ADMIN)
    db.session.add(new_user)
    db.session.commit()
    print("Account successfully created! "
          "Password is 'Change4me' by default. Please change password after initial login")

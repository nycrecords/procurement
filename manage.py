from werkzeug.security import generate_password_hash
import os
from app import create_app, db
from app.models import User, Request
from app.constants import division, roles
from flask import url_for
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Request=Request)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def list_routes():
    import urllib
    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = urllib.parse.unquote("{:50s} {:20s} {}".format(
                                                        rule.endpoint,
                                                        methods,
                                                        url
                                                        )
                              )
        output.append(line)

    for line in sorted(output):
        print(line)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def create_admin(first_name, last_name, email, division=division.MRMD):
    with app.app_context():
        newuser = User(email=email,
                       division=division,
                       password_hash=generate_password_hash("Change4me"),
                       first_name=first_name,
                       last_name=last_name,
                       role=roles.ADMIN)
        db.session.add(newuser)
        print("Account successfully created! "
              "Password is 'Change4me' by default. Please change password after initial login")


if __name__ == '__main__':
    manager.run()

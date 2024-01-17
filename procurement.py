import os
from datetime import datetime
from uuid import uuid4

from flask_migrate import Migrate
from app import create_app, db
from app.constants.roles import USER_ROLES
from app.models import User, Role

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)


@app.cli.command()
def create_test_user():
    user = User(guid=uuid4().hex, email='test@email.com', is_active=True, last_sign_in_at=datetime.utcnow())
    db.session.add(user)
    db.session.commit()


@app.cli.command()
def assign_admin_role():
    user_email = input("Enter user email: ")
    user = User.query.filter_by(email=user_email).first()

    if user:
        admin_role = Role.query.filter_by(name='admin').first()
        user.roles = [admin_role]
        user.is_active = True
        db.session.add(user)
        db.session.commit()
    else:
        print("User not found.")
        return

    print("Successfully assigned admin role to user " + user_email)


@app.cli.command()
def create_user_roles():
    roles_to_add = []

    for role in USER_ROLES:
        roles_to_add.append(role)

    existing_roles = Role.query.filter(Role.name.in_(roles_to_add)).all()
    existing_role_names = set(role.name for role in existing_roles)

    roles_to_create = [Role(name=role_name) for role_name in roles_to_add if role_name not in existing_role_names]

    if roles_to_create:
        db.session.add_all(roles_to_create)
        db.session.commit()

        print("Successfully created user roles.")


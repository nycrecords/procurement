from datetime import datetime

from flask_login import current_user

from app import db
from app.auth.utils import create_auth_event
from app.constants import auth_event_type, roles
from app.models import Role, User


def assign_user_role(user_guid: str, new_role_name: str):
    """
    Assign a new role to a user and create an authentication event.

    Args:
        user_guid (str): The GUID of the user.
        new_role_name (str): The name of the new role.

    Returns:
        None
    """
    user = User.query.filter_by(guid=user_guid).one_or_none()

    if user:
        if new_role_name == 'inactive':
            deactivate_user(user)
        else:
            old_role = user.role if user.roles else None
            new_role = Role.query.filter_by(name=new_role_name).one_or_none()

            if new_role:
                user.roles = [new_role]
                user.is_active = True
                user.updated_at = datetime.utcnow()
                db.session.commit()

                create_auth_event(
                    user_guid=current_user.guid,
                    auth_event_type=auth_event_type.USER_ROLE_CHANGED if old_role else auth_event_type.AGENCY_USER_ACTIVATED,
                    previous_value={'role': old_role if old_role else None, 'user_email': user.email,
                                    'user_guid': user.guid, },
                    new_value={'role': new_role.name, 'user_email': user.email, 'user_guid': user.guid, }
                )


def deactivate_user(user: User):
    """
    Deactivate a user and create an authentication event.

    Args:
        user (Users): The user to deactivate.

    Returns:
        None
    """
    user_role = user.role
    user.roles = []
    user.is_active = False
    db.session.commit()

    create_auth_event(
        user_guid=current_user.guid,
        auth_event_type=auth_event_type.AGENCY_USER_DEACTIVATED,
        previous_value={'role': user_role, 'user_email': user.email, 'user_guid': user.guid, },
        new_value={'role': None, 'user_email': user.email, 'user_guid': user.guid, }
    )


def assign_user_division(user_guid: str, new_division_name: str):
    """
    Assign a new division to a user and create an authentication event.

    Args:
        user_guid (str): The GUID of the user.
        new_division_name (str): The name of the new role.

    Returns:
        None
    """
    user = User.query.filter_by(guid=user_guid).one_or_none()

    if user:
        if new_division_name == 'none':
            deactivate_user(user)
        else:
            old_division = user.division if user.divisions else None
            new_division = Role.query.filter_by(name=new_division_name).one_or_none()

            if new_division:
                user.division = new_division
                user.is_active = True
                user.updated_at = datetime.utcnow()
                db.session.commit()

                create_auth_event(
                    user_guid=current_user.guid,
                    auth_event_type=auth_event_type.USER_DIVISION_CHANGED,
                    previous_value={'division': old_division if old_division else None, 'user_email': user.email,
                                    'user_guid': user.guid, },
                    new_value={'division': new_division.name, 'user_email': user.email, 'user_guid': user.guid, }
                )

"""
    ..module: utils


"""
from werkzeug.security import check_password_hash
from ..models import User
import re


def check_password_requirements(email, old_password, password, password_confirmation):
    """
    Check a password against security requirements.

    :param email: Email of user
    :param old_password: Original password
    :param password: Password that needs to be checked.
    :param password_confirmation: Confirmation of new password
    :return: Boolean (True if valid, False if not)
    """

    user_password = User.query.filter_by(email=email).first().password_hash

    if not check_password_hash(pwhash=user_password, password=old_password):
        return False

    if password != password_confirmation:
        return False

    if not re.match(r'[A-Za-z0-9@#$%^&+=]{8,128}', password):
        return False

    return True

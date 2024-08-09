"""
Utility functions used for database operations
"""
import sys

from flask import current_app, flash
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.attributes import flag_modified

from app import db


def create_object(obj):
    """
    A utility function to add an object to the database
    :param obj: the object that is being added to the database
    :return: no return value, an object will be added to the database
    """
    try:
        db.session.add(obj)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print("Failed to CREATE {} : {}".format(obj, e))
        print(sys.exc_info())


def update_object(data, obj_type, obj_id, by_guid=False):
    """
    Update a database record.
    :param data: a dictionary of attribute-value pairs
    :param obj_type: sqlalchemy model
    :param obj_id: id of record
    :param by_guid: boolean indicating whether identifier is a guid
    :return: was the record updated successfully?
    """
    if by_guid:
        obj = get_object_by_guid(obj_type, obj_id)
    else:
        obj = get_object(obj_type, obj_id)

    if obj:
        for attr, value in data.items():
            if isinstance(value, dict):
                # update json values
                attr_json = getattr(obj, attr) or {}
                for key, val in value.items():
                    attr_json[key] = val
                setattr(obj, attr, attr_json)
                flag_modified(obj, attr)
            else:
                setattr(obj, attr, value)
        try:
            db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
            current_app.logger.exception("Failed to UPDATE {}".format(obj))
            return False


def get_object(obj_type, obj_id):
    """
    Safely retrieve a database record by its id
    and its sqlalchemy object type.
    """
    if not obj_id:
        return None
    try:
        return obj_type.query.get(obj_id)
    except SQLAlchemyError:
        db.session.rollback()
        current_app.logger.exception('Error searching "{}" table for id {}'.format(
            obj_type.__tablename__, obj_id))
        return None


def get_object_by_guid(model, guid):
    """
    Retrieve an object from the database by its GUID.
    :param model: The SQLAlchemy model class representing the database table
    :param guid: The globally unique identifier for the object
    :return: The object if found, None otherwise
    """
    try:
        return model.query.filter_by(guid=guid).first()
    except SQLAlchemyError as e:
        current_app.logger.exception("Database error occurred while retrieving object by GUID: {}".format(e))
        return None


def update_user_information(form, fields, user):
    """
    Updates the user's information based on the form data submitted via a POST request.

    :param form: The form object containing the submitted data.
    :param fields: The form fields containing the submitted data.
    :param user: The user object whose information is to be updated.
    :return: Flash message
    """
    changes_made = False

    for field in fields:
        form_data = str(getattr(form, field).data)
        if getattr(user, field) != form_data:
            setattr(user, field, form_data)
            changes_made = True

    if changes_made:
        try:
            db.session.commit()
            return flash('User information successfully updated!', 'success')
        except Exception as e:
            db.session.rollback()
            return flash('An error occurred while updating the user.', 'warning')
    else:
        return flash('No user changes made.', 'info')

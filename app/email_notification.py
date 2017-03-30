"""
.. module: email_notification.

    :synopsis: Defines email functionality for the application
"""
from flask import current_app, render_template
from flask_mail import Message
from app import mail
from threading import Thread


def get_mime_type(filepath):
    index = -1
    while filepath[index] != '.' and abs(index) < len(filepath):
        index -= 1
    return filepath[index + 1:]


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to_list, subject, template, file_path=None, **kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=to_list)
    # msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    if file_path is not None:
        with app.open_resource(file_path) as fp:
            msg.attach(file_path, get_mime_type(file_path), fp.read())

    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr

"""
.. module: email_notification.

    :synopsis: Defines email functionality for the application
"""
from flask import current_app, render_template
from flask_mail import Message
from app import mail
from threading import Thread
import mimetypes


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
            ctype, encoding = mimetypes.guess_type(file_path)
            if ctype is None or encoding is not None:
                # No guess could be made, or the file is encoded (compressed), so
                # use a generic bag-of-bits type.
                ctype = 'application/octet-stream'
            msg.attach(file_path, ctype, fp.read())

    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr

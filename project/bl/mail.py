from flask_mail import Message
from project import mail, app
# TODO: прикрутить celery


def send_mail(title, body, recipients=None, file=None):
    if recipients is None:
        recipients = [app.config['MAIL_TO_SEND']]
    msg = Message(title, recipients=recipients)
    msg.body = body
    if file:
        file_name, file_type, file_bytes = file
        msg.attach(file_name, file_type, file_bytes)
    mail.send(msg)

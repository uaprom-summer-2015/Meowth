from flask_mail import Message
from project import mail, app
# TODO: прикрутить celery


def send_mail(title, body, recipients=None, attachment=None):
    if recipients is None:
        recipients = [app.config['MAIL_TO_SEND']]
    msg = Message(title, recipients=recipients)
    msg.body = body
    if attachment:
        msg.attach(attachment.filename,
                   attachment.content_type,
                   attachment.read())
    mail.send(msg)

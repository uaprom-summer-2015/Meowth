from flask_mail import Message
from project import mail, app
# TODO: прикрутить selery


def send_mail(title, body, file_name=None,
              file_type=None, file_bytes=None):
    msg = Message(title,
                  recipients=[app.config['MAIL_TO_SEND']])
    msg.body = body
    if file_name:
        msg.attach(file_name, file_type, file_bytes)
    mail.send(msg)

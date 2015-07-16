from flask import request
from flask_mail import Message
from project import mail, app
# TODO: прикрутить celery


def send_mail(title, body, recipients, attachment_name=None,
              attachment_type=None, attachment=None):
    msg = Message(title, recipients=recipients)
    msg.body = body
    if attachment:
        msg.attach(attachment_name,
                   attachment_type,
                   attachment.read())
    mail.send(msg)


def mail_from_aplly_form(form, recipitiens=None, title=None):
    if recipitiens is None:
        recipitiens = [app.config['MAIL_TO_SEND']]
    if title is None:
        title = 'Ответ на вакансию'
    body = 'Имя: {}\n' \
           'Email: {}\n' \
           'Телефон: {}'.format(form.name.data,
                                form.email.data, form.phone.data)
    if form.comment.data:
        body += '\nКоментарий: {}'.format(form.comment.data)
    attachment = request.files[form.attachment.name]

    send_mail(title, body, recipitiens, attachment.filename,
              attachment.content_type, attachment)

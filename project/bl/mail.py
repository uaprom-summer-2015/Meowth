from flask import request
from flask_mail import Message
from project import app
from project.tasks.mail import celery_send_mail


def get_message(title, body, recipients, attachment_name=None,
                attachment_type=None, attachment=None):
    msg = Message(title, recipients=recipients)
    msg.body = body
    if attachment:
        msg.attach(attachment_name,
                   attachment_type,
                   attachment.read())
    return msg


def get_message_from_form(form, vacancy):
    recipitiens = [app.config['MAIL_TO_SEND']]
    title = 'Ответ на вакансию: {}'.format(vacancy.title)
    body = 'Ответ на вакансию: {}\n' \
    'Имя: {}\n' \
    'Email: {}\n' \
    'Телефон: {}'.format(
        vacancy.title,
        form.name.data,
        form.email.data,
        form.phone.data,
    )
    if form.comment.data:
        body += '\nКоментарий: {}'.format(form.comment.data)

    attachment = request.files[form.attachment.name]

    return get_message(title, body, recipitiens, attachment.filename,
                       attachment.content_type, attachment)


def send_mail_from_form(form, vacancy):
    msg = get_message_from_form(form, vacancy)
    celery_send_mail.delay(msg)


def send_mail(title, body, recipients, attachment_name=None,
              attachment_type=None, attachment=None):
    msg = get_message(title, body, recipients, attachment_name,
                      attachment_type, attachment)
    celery_send_mail.delay(msg)


from email.policy import EmailPolicy
from flask import request
import flask_mail
from config import Hardcoded
from project.bl.utils import BaseBL
from project.tasks.mail import celery_send_mail


class MailTemplateBL(BaseBL):
    pass


flask_mail.message_policy = EmailPolicy(linesep='\r\n', refold_source='none')


def get_message(title, recipients, body=None, html=None, attachment_name=None,
                attachment_type=None, attachment=None):
    msg = flask_mail.Message(title, recipients=recipients)
    if body:
        msg.body = body
    if html:
        msg.html = html
    if attachment:
        msg.attach(attachment_name,
                   attachment_type,
                   attachment.read())
    return msg


def get_message_from_form(form, vacancy):
    recipients = [Hardcoded.MAIL_TO_SEND]
    title = 'Ответ на вакансию: {}'.format(vacancy.title)
    body = 'Ответ на вакансию: {}\n' \
           'Имя: {}\n' \
           'Email: {}\n' \
           'Телефон: {}'.format(vacancy.title,
                                form.name.data,
                                form.email.data,
                                form.phone.data,
                                )
    if form.comment.data:
        body += '\nКоментарий: {}'.format(form.comment.data)

    attachment = request.files[form.attachment.name]

    return get_message(
        title=title,
        recipients=recipients,
        body=body,
        attachment_name=attachment.filename,
        attachment_type=attachment.content_type,
        attachment=attachment
    )


# noinspection PyUnresolvedReferences
def send_mail_from_form(form, vacancy):
    msg = get_message_from_form(form, vacancy)
    msg4reply = get_msg_for_reply(form, vacancy)
    celery_send_mail.delay(msg)
    celery_send_mail.delay(msg4reply)


# noinspection PyUnresolvedReferences
def send_mail(title, recipients, body=None, html=None, attachment_name=None,
              attachment_type=None, attachment=None):
    msg = get_message(title, recipients, body, html, attachment_name,
                      attachment_type, attachment)
    celery_send_mail.delay(msg)


def get_msg_for_reply(form, vacancy):
    from project.models import MailTemplate
    mail_temp = MailTemplate.query.filter(
        MailTemplate.title=='Подтверждение получения резюме'
    ).one()
    recipients = [form.email.data]
    subject = mail_temp.subject
    html = mail_temp.html
    return get_message(
        title=subject,
        html=html,
        recipients=recipients
    )


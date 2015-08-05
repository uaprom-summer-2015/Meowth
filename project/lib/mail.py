from flask import request
from html2text import html2text
from jinja2 import Template
from config import Hardcoded
from project.tasks.mail import celery_send_mail
from email.policy import EmailPolicy
from project.models import MailTemplate
import flask_mail

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
    kwargs = {
        'name': form.name.data,
        'email': form.email.data,
        'phone': form.phone.data,
        'comment': form.comment.data,
        'title': vacancy.title,
    }

    mail_temp = MailTemplate.query.filter(
        MailTemplate.title == 'Уведомление о новом резюме'
    ).one()

    subject = Template(mail_temp.subject).render(**kwargs)
    html = Template(mail_temp.html).render(**kwargs)
    attachment = request.files[form.attachment.name]
    body = html2text(html)

    return get_message(
        title=subject,
        recipients=recipients,
        html=html,
        attachment_name=attachment.filename,
        attachment_type=attachment.content_type,
        attachment=attachment,
        body=body,
    )


def send_mail_from_form(form, vacancy):
    celery_send_mail.delay(get_message_from_form(form, vacancy))
    celery_send_mail.delay(get_msg_for_reply(form, vacancy))


def send_mail(title, recipients, **kwargs):
    msg = get_message(title, recipients, **kwargs)
    celery_send_mail.delay(msg)


def get_msg_for_reply(form, vacancy):
    kwargs = {
        'name': form.name.data,
        'title': vacancy.title,
    }
    mail_temp = MailTemplate.query.filter(
        MailTemplate.title == 'Подтверждение получения резюме'
    ).one()

    recipients = [form.email.data]
    subject = Template(mail_temp.subject).render(**kwargs)
    html = Template(mail_temp.html).render(**kwargs)
    body = html2text(html)
    return get_message(
        title=subject,
        html=html,
        recipients=recipients,
        body=body,
    )

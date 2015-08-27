import os
from flask import request, current_app, render_template
from html2text import html2text
from string import Template
import magic
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


def get_message_from_form(form, vacancy_title):
    recipients = current_app.config["MAILS_TO_SEND"]
    kwargs = {
        'name': form.name.data,
        'email': form.email.data,
        'phone': form.phone.data,
        'comment': form.comment.data,
        'title': vacancy_title,
    }

    mail_temp = MailTemplate.bl.get(MailTemplate.MAIL.CV)

    subject = mail_temp.subject
    html = Template(mail_temp.html).safe_substitute(**kwargs)
    html = jinja_render_template(html)
    attachment = request.files[form.attachment.name]
    body = html2text(html)

    msg = get_message(
        title=subject,
        recipients=recipients,
        html=html,
        attachment_name=attachment.filename,
        attachment_type=attachment.content_type,
        attachment=attachment,
        body=body,
    )

    msg = add_image(msg, 'logo-with-text.png')
    return msg


def send_mail_from_form(form, vacancy_title):
    celery_send_mail.delay(get_message_from_form(form, vacancy_title))
    celery_send_mail.delay(get_msg_for_reply(form, vacancy_title))


def send_mail(title, recipients, **kwargs):
    msg = get_message(title, recipients, **kwargs)
    celery_send_mail.delay(msg)


def get_msg_for_reply(form, vacancy_title):
    kwargs = {
        'name': form.name.data,
        'title': vacancy_title,
    }
    mail_temp = MailTemplate.bl.get(MailTemplate.MAIL.REPLY)

    recipients = [form.email.data]
    subject = mail_temp.subject
    html = Template(mail_temp.html).safe_substitute(**kwargs)
    html = jinja_render_template(html)
    body = html2text(html)
    msg = get_message(
        title=subject,
        html=html,
        recipients=recipients,
        body=body,
    )

    msg = add_image(msg, 'logo-with-text.png')
    return msg


def offer_cv_send_mail(form):
    celery_send_mail.delay(get_message_from_form(form, 'Предложить резюме'))


def jinja_render_template(text):
    host = request.host_url
    return render_template(
        'mail.html',
        host=host,
        text=text,
        cid='logo-with-text.png',
    )


def add_image(msg, img_name):
    img_path = os.path.join(current_app.config["BASEDIR"], 'project/static/img', img_name)
    headers = [('Content-ID', '<{}>'.format(img_name))]
    with open(img_path, 'rb') as f:
        content_type = magic.from_file(img_path, mime=True).decode()
        msg.attach(
            filename=img_name,
            data=f.read(),
            content_type=content_type,
            headers=headers,
        )
    return msg

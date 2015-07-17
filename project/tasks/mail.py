from project import celery
from project import mail


@celery.task()
def celery_send_mail(msg):
    mail.send(msg)

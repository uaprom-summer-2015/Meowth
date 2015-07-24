from project.extensions import celery, mail


@celery.task()
def celery_send_mail(msg):
    mail.send(msg)

from config import settings
from django.core.mail import get_connection, EmailMessage
from celery import shared_task
from config.celery import app


@app.task
def send_auth_email(subject, body, receiver, data=None):

    default_mail_settings = settings.MULTIPLE_MAIL_SETTINGS.get('default')

    try:
        with get_connection(
                host=default_mail_settings.get('host'),
                port=default_mail_settings.get('port'),
                username=default_mail_settings.get('user'),
                password=default_mail_settings.get('password'),
                user_tls=default_mail_settings.get('tls')
        ) as connection:
            mail = EmailMessage(subject, body, default_mail_settings.get('user'), [receiver],
                                connection=connection)
            mail.content_subtype = 'html'
            mail.send()
    except Exception as e:
        print('************EMAIL ERROR***********')
        print(e)
        pass


@app.task
def send_auth_email_test():
    print("Hello celery runs")
    return "This is my world"


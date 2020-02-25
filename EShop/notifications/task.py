from celery import shared_task
from django.core.mail import send_mail
from mysite.local_settings import username
from .models import Notificator
import logging


logger = logging.getLogger(username)
logger.setLevel(logging.INFO)
fh = logging.FileHandler('/home/jaro/PycharmProjects/EShop/notifications/test.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s - %(name)s')
fh.setFormatter(formatter)
logger.addHandler(fh)


"""
logging.basicConfig(
    filename='test.log',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s:%(name)s'
)
"""


@shared_task
def send_email_task():
    title = 'Celery worked'
    text = 'Ah well, here we go again...'
    mailer = username
    mail_deliver = ['kefowe9465@xhyemail.com']
    send_mail(title, text, mailer, mail_deliver)
    return logger.info(send_email_task)

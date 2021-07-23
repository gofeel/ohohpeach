from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from django.core.mail import send_mail
from threading import Thread
import requests

from django.conf import settings


def post_message(instance):
    msg = "New Order - %s" % (instance, )
    token = settings.NOTIFICATION_TELEGRAM_TOKEN
    data = {
        'chat_id': settings.NOTIFICATION_TELEGRAM_CHATROOM,
        'text': msg
    }
    requests.post("https://api.telegram.org/bot%s/sendMessage" % (token,), data=data)

    fields = ['product', 'qty', 'buyer', 'buyer_contact', 'sender', 'recipient', 'recipient_phone_number', 'recipient_zipcode', 'recipient_base_address', 'recipient_additional_address', 'memo', 'shipping_option']

    result = ""
    for f in fields:
        result += "%s:%s\r\n" % (f, getattr(instance, f))

    send_mail(
        u'[%s] 새로운 주문 - %s' % (settings.SITE_NAME, instance,),
        result,
        settings.NOTIFICATION_EMAIL_SENDER,
        [settings.NOTIFICATION_EMAIL_SENDER],
        fail_silently=False,
    )

    instance.notify(Order.NotificationType.CONFIRMED)


@receiver(post_save, sender=Order)
def model_post_save(sender, instance, **kwargs):
    if kwargs['created']:
        if settings.NOTIFICATION:
            t = Thread(target=post_message, args=(instance,))
            t.start()

# -*- coding: utf-8 -*-
from enum import Enum

import base62
from django.conf import settings
from django.core.mail import send_mail
from django.db import models

from .tools import sendsms


class Product(models.Model):
    name = models.CharField(max_length=30)
    price = models.IntegerField(default=0)
    call_name = models.CharField(max_length=30, default="")
    enabled = models.BooleanField(default=True, blank=True)

    class Meta:
        verbose_name = u'상품'
        verbose_name_plural = u'상품'

    def __str__(self):
        return "%s / %d원" % (self.name, self.price)


class OrderManager(models.Manager):
    def get_with_hid(self, hid):
        h = base62.decode(hid)
        i = h ^ settings.HKEY
        i = i >> settings.HP
        return self.get(id=i)


class Order(models.Model):
    product = models.ForeignKey(Product, models.SET_NULL, verbose_name=u"상품", null=True, blank=True)
    qty = models.IntegerField(default=0)
    buyer = models.CharField("주문자 이름", max_length=30, default="", null=False, blank=False)
    buyer_contact = models.CharField("주문자 연락처", max_length=255, default="", null=True, blank=False)
    buyer_contact_type = models.PositiveSmallIntegerField(default=0, blank=True)
    sender = models.CharField("입금자 이름", max_length=30, default="", null=True, blank=False)
    recipient = models.CharField("받는 사람", max_length=30, default="", null=True, blank=False)
    recipient_phone_number = models.CharField("받는사람 전화번호", max_length=20, default="", null=True, blank=False)
    recipient_zipcode = models.CharField("우편번호", max_length=5, default="", null=True, blank=False)
    recipient_base_address = models.CharField("주소", max_length=300, default="", null=True, blank=False)
    recipient_additional_address = models.CharField("상세주소", max_length=300, default="", null=True, blank=True)
    memo = models.TextField("특이사항", default="", null=True, blank=True)
    shipping_memo = models.CharField(max_length=300, default="", null=True, blank=True)
    shipping_option = models.PositiveSmallIntegerField(default=0, blank=True)

    status_payment = models.BooleanField(default=False, blank=True)
    status_payment_sms = models.BooleanField(default=False, blank=True)
    status_shipping = models.BooleanField(default=False, blank=True)

    shipping_order = models.PositiveSmallIntegerField(default=0, blank=True)
    shipping_id = models.PositiveSmallIntegerField(default=0, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    @property
    def pn(self):
        value = self.recipient_phone_number
        if value is None:
            return ""
        phone = '%s-%s-%s' % (value[0:3], value[3:7], value[7:11])
        return phone

    @property
    def hid(self):
        k = self.id << settings.HP
        return base62.encode(k ^ settings.HKEY)

    def sum(self):
        return self.qty * self.product.price

    class NotificationType(Enum):
        CONFIRMED, COMPLETED, SHIPPED = range(3)

    def notify(self, type):
        if type == self.NotificationType.CONFIRMED:
            title = '주문확인되었습니다'
            message = '주문확인되었습니다. 상세주문내역확인 https://neungju.com/order/v/%s' % (self.hid,)  # Message
        elif type == self.NotificationType.COMPLETED:
            title = '입금이 확인되었습니다'
            message = '입금이 확인되었습니다. 상세주문내역확인 https://neungju.com/order/v/%s' % (self.hid,)  # Message
        elif type == self.NotificationType.SHIPPED:
            title = '배송이 시작되었습니다'
            message = '배송이 시작되었습니다. 상세주문내역확인 https://neungju.com/order/v/%s' % (self.hid,)  # Message
        if self.buyer_contact_type == 0:
            sendsms(self.buyer_contact, message)
        else:
            send_mail(
                u'[복숭아] %s' % (title,),
                message,
                settings.NOTIFICATION_EMAIL_SENDER,
                [self.buyer_contact],
                fail_silently=False,
            )

    def __str__(self):
        try:
            name = "%d - %s/%s/%d" % (self.id, self.buyer, self.product.name, self.qty)
        except TypeError:
            name = "<<ERROR>>"
        return name

    objects = OrderManager()

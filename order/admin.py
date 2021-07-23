from django.contrib import admin
from .models import Order, Product


def make_payment_checked(modeladmin, request, queryset):
    queryset.update(status_payment=True)


make_payment_checked.short_description = "입금확인"


def make_shipping_checked(modeladmin, request, queryset):
    queryset.update(status_shipping=True)
    for order in queryset:
        order.notify(Order.NotificationType.SHIPPED)


make_shipping_checked.short_description = "배송중"


def make_payment_sms_checked(modeladmin, request, queryset):
    queryset.update(status_payment=True)
    queryset.update(status_payment_sms=True)
    for order in queryset:
        order.notify(Order.NotificationType.COMPLETED)


make_payment_sms_checked.short_description = "입금확인 및 문자전송"


def send_reminder(modeladmin, request, queryset):
    for order in queryset:
        order.notify(Order.NotificationType.CONFIRMED)


send_reminder.short_description = "확인문자전송"


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'shipping_id', 'status', 'buyer', 'product', 'qty', 'sum', 'sender', 'recipient',
                    'recipient_base_address', 'recipient_additional_address', 'memo', 'shipping_option']
    search_fields = ['buyer', 'sender', 'recipient', 'memo', 'buyer_contact']
    actions = [make_payment_checked, make_payment_sms_checked, make_shipping_checked, send_reminder]

    def status(self, obj):
        rtn = ""
        rtn = rtn + ("✅" if obj.status_payment else "❌")
        rtn = rtn + ("💌" if obj.status_payment_sms else "⬜️")
        rtn = rtn + ("📦" if obj.status_shipping else "❌")
        return rtn


admin.site.register(Order, OrderAdmin)
admin.site.register(Product)

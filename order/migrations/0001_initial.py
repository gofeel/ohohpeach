# Generated by Django 3.2.5 on 2021-07-23 16:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('price', models.IntegerField(default=0)),
                ('call_name', models.CharField(default='', max_length=30)),
                ('enabled', models.BooleanField(blank=True, default=True)),
            ],
            options={
                'verbose_name': '상품',
                'verbose_name_plural': '상품',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField(default=0)),
                ('buyer', models.CharField(default='', max_length=30, verbose_name='주문자 이름')),
                ('buyer_contact', models.CharField(default='', max_length=255, null=True, verbose_name='주문자 연락처')),
                ('buyer_contact_type', models.PositiveSmallIntegerField(blank=True, default=0)),
                ('sender', models.CharField(default='', max_length=30, null=True, verbose_name='입금자 이름')),
                ('recipient', models.CharField(default='', max_length=30, null=True, verbose_name='받는 사람')),
                ('recipient_phone_number', models.CharField(default='', max_length=20, null=True, verbose_name='받는사람 전화번호')),
                ('recipient_zipcode', models.CharField(default='', max_length=5, null=True, verbose_name='우편번호')),
                ('recipient_base_address', models.CharField(default='', max_length=300, null=True, verbose_name='주소')),
                ('recipient_additional_address', models.CharField(blank=True, default='', max_length=300, null=True, verbose_name='상세주소')),
                ('memo', models.TextField(blank=True, default='', null=True, verbose_name='특이사항')),
                ('shipping_memo', models.CharField(blank=True, default='', max_length=300, null=True)),
                ('shipping_option', models.PositiveSmallIntegerField(blank=True, default=0)),
                ('status_payment', models.BooleanField(blank=True, default=False)),
                ('status_payment_sms', models.BooleanField(blank=True, default=False)),
                ('status_shipping', models.BooleanField(blank=True, default=False)),
                ('shipping_order', models.PositiveSmallIntegerField(blank=True, default=0)),
                ('shipping_id', models.PositiveSmallIntegerField(blank=True, default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.product', verbose_name='상품')),
            ],
        ),
    ]

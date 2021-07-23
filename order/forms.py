from django.forms import ModelForm
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django import forms
from .models import Order, Product
import re


class OrderForm(ModelForm):

    product = forms.ModelChoiceField(label=u"상품", queryset=Product.objects.filter(enabled=True))
    memo = forms.CharField(label=u"특이사항/메모 - 추천인, 토요일 택배 수령, 등등", required=False, widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}))

    def clean(self):
        cleaned_data = super().clean()
        t = cleaned_data['buyer_contact_type']
        if 'buyer_contact' in self.cleaned_data:
            if t == 0:
                cleaned_data['buyer_contact'] = self.clean_phone_number(cleaned_data['buyer_contact'])
                if not cleaned_data['buyer_contact']:
                    msg = '전화번호 형식에 문제가 있습니다.'
                    self.add_error('buyer_contact', msg)
            else:
                validate_email(cleaned_data['buyer_contact'])
        else:
            msg = '연락처가 비어 있습니다.'
            self.add_error('buyer_contact', msg)
        return cleaned_data

    def clean_recipient_phone_number(self):
        data = self.cleaned_data['recipient_phone_number']
        if data is None:
            try:
                data = self.cleaned_data['buyer_contact']
            except KeyError:
                raise ValidationError('받는 사람 연락처가 비어 있습니다.')
        data = self.clean_phone_number(data)
        if data is None:
            raise ValidationError('잘못된 연락처 입니다.')
        return data

    @staticmethod
    def clean_phone_number(s):
        if s is not None:
            return re.sub(r'[^\d]', '', s)
        else:
            return ''

    class Meta:
        model = Order
        fields = ['product', 'qty', 'buyer', 'buyer_contact', 'buyer_contact_type', 'sender', 'recipient', 'recipient_phone_number', 'recipient_zipcode', 'recipient_base_address', 'recipient_additional_address', 'memo', 'shipping_option']

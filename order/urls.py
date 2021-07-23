from django.urls import path, re_path
from . import views

app_name = 'order'


urlpatterns = [
    path('', views.index, name='index'),
    path('add', views.add_order, name='add-order'),
    re_path(r'v/(?P<hid>.+)$', views.read_order_hid, name='read-order-hid'),
    path('browse', views.browse_order, name='browse'),
    path('filter', views.filter_order, name='filter'),
    re_path(r'send/(?P<order_id>.+)$', views.send_order, name='send-order'),
]

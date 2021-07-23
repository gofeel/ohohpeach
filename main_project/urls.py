from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', RedirectView.as_view(url='order/', permanent=False)),
    path('admin/', admin.site.urls),
    path('order/', include('order.urls')),
]

urlpatterns += staticfiles_urlpatterns()

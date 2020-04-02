from django.conf.urls import url
from django.urls import include
from django.contrib import admin

urlpatterns = [
    url('', include('core.urls')),
    url('admin/', admin.site.urls),
]

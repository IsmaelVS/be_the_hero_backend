from django.urls import path
from django.contrib import admin

from core import views


urlpatterns = [
    path('ongs/', views.ongs),
    path('incidents/', views.incidents),
    path('incidents/<int:id>/', views.incident),
    path('incidents/ong/', views.list_incidents_from_an_ong),
    path('login/', views.login),
    path('admin/', admin.site.urls),
]

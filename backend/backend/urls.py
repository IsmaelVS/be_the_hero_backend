"""URLs to all project."""
from django.urls import path
from django.contrib import admin

from core import views


urlpatterns = [
    path('ongs/', views.OngsView.as_view()),
    path('incidents/', views.IncidentsView.as_view()),
    path('incidents/<int:id>/', views.DeleteIncidentView.as_view()),
    path('incidents/ong/', views.ListIncidentFromAnONGView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('admin/', admin.site.urls),
]

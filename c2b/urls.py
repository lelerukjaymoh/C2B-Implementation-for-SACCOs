from django.urls import path
from c2b import views

urlpatterns = [
    path('', views.home, name='home'),
]

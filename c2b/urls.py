from django.urls import path
from c2b import views
from c2b.views import TransactionsListView

urlpatterns = [
    path('register_url', views.register_url, name='register_url'),
    path('api/v1/c2b/validation', views.validation, name='validation'),
    path('api/v1/c2b/confirmation', views.confirmation, name='confirmation'),
    path('transactions', TransactionsListView.as_view()),
]

from django.urls import path
from c2b import views
from c2b.views import TransactionsListView

urlpatterns = [
    path('', views.home, name='home'),
    path('validation', views.validation, name='validation'),
    path('confirmation', views.confirmation, name='confirmation'),
    path('transactions', TransactionsListView.as_view()),
]

from django.urls import path
from . import views

urlpatterns = [
    path("", views.get_all_contracts, name="contracts"),
    path("/<int:pk>/transactions", views.get_contract_transactions, name="transactions"),
]
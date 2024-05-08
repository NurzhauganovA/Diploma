from django.urls import path
from . import views

urlpatterns = [
    path("", views.get_all_contracts, name="contracts"),
    path("app/<int:pk>", views.get_contract_info, name="contract_info"),
    path(
        "app/<str:contract_number>",
        views.change_contract_data,
        name="change_contract_data",
    ),
    path(
        "app/<int:pk>/transactions",
        views.get_contract_transactions,
        name="transactions",
    ),
    path("app/contracts/export", views.get_contracts_export, name="export_contract"),
]
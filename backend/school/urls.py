from django.urls import path
from . import views

urlpatterns = [
    path('school-part', views.school_part, name='school-part'),
    path("schools/<int:pk>/", views.get_people, name="get_people"),
    path("users/<int:pk>/", views.get_more_info, name="get_more_info"),
    path("contracts/<int:pk>/", views.get_contract_info, name="get_contract_info"),

    path("contracts/<int:pk>/transactions/", views.get_contract_transactions, name="get_contract_transactions"),
    path("contracts/<int:pk>/create_transaction/", views.create_transaction, name="create_transaction"),
    path("contracts/<int:pk>/edit_transaction/", views.edit_transaction, name="edit_transaction"),
    path("contracts/<int:pk>/delete_transaction/", views.delete_transaction, name="delete_transaction"),

    path("distribution", views.distribution, name="distribution"),

    path("distribution/add_new_statement", views.add_new_statement, name="add_new_statement"),
    path("distribution/add_new_class", views.add_new_class, name="add_new_class"),

    path("distribution/approve-to-class", views.approve_to_class, name="approve_to_class"),
    path("distribution/remove-from-class", views.remove_from_class, name="remove_from_class"),
]

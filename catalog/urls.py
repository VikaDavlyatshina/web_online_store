from django.urls import path
from catalog.apps import CatalogConfig
from . import views

from catalog.views import product_details

app_name = CatalogConfig.name


urlpatterns = [
    path("home/", views.home, name="home"),
    path("contacts/", views.contacts, name="contacts"),
    path("product/<int:pk>/", views.product_details, name="product_details"),
]

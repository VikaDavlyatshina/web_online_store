from django.urls import path
from catalog.apps import CatalogConfig
from . import views

from catalog.views import ProductDetailView, ProductListView

app_name = CatalogConfig.name


urlpatterns = [
    path("", ProductListView.as_view(), name="product_list"),
    path("contacts/", views.contacts, name="contacts"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product_details"),
    path("product_add/", views.product_add, name="product_add"),
]

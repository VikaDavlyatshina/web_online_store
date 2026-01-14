from django.urls import path
from catalog.apps import CatalogConfig
from . import views

from catalog.views import ProductDetailView, ProductListView, ContactsView, ProductCreateView

app_name = CatalogConfig.name


urlpatterns = [
    path("", ProductListView.as_view(), name="product_list"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product_details"),
    path("product_add/", ProductCreateView.as_view(), name="product_add"),
]

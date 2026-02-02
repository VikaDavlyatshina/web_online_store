from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import ContactsView, ProductCreateView, ProductDetailView, ProductListView, ProductUpdateView, \
    ProductDeleteView

app_name = CatalogConfig.name


urlpatterns = [
    path("", ProductListView.as_view(), name="product_list"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product_details"),
    path("product_add/", ProductCreateView.as_view(), name="product_add"),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path("contacts/", ContactsView.as_view(), name="contacts"),
]

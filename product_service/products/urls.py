from django.urls import path
from .views import ProductView, ProductDetailView


urlpatterns = [
    path("v1/all", ProductView.as_view({
        "get": "list",
        "post": "create"
    }), name="product-create"),
    path("v1/<str:id>", ProductDetailView.as_view({
        "get": "retrieve",
        "put": "update",
        "delete": "destroy"
    }), name="product-detail")
]

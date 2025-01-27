from django.urls import path
from .views import InventoryView, InventoryDetailView


urlpatterns = [
    path("v1/all", InventoryView.as_view({
        "get": "list",
        "post": "create"
    })),
    path("v1/<str:id>", InventoryDetailView.as_view({
        "get": "retrieve",
        "put": "update",
        "delete": "destroy"
    }))
]

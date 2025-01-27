from django.urls import path
from .views import OrderView, OrderViewSet

urlpatterns = [
    path('add/', OrderView.as_view(), name='order-list-create'),
    path('addset/', OrderViewSet.as_view({
        "post": "create",
    }), name='order-viewset'),
]
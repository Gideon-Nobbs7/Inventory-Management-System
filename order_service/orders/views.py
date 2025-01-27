from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes
from rest_framework import status
from .serializers import OrderSerializer
from .models import Order
from .authentication import MicroserviceAuthentication

@method_decorator(csrf_exempt, name="dispatch")
class OrderView(APIView):
     authentication_classes = [MicroserviceAuthentication]
     permission_classes = [IsAuthenticated]

     def post(self, request):
          serializer =  OrderSerializer(data=request.data, context={"request": request})
          if serializer.is_valid():
               serializer.save()
               return Response(serializer.data, status=status.HTTP_201_CREATED)
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     

class OrderViewSet(viewsets.ModelViewSet):
     authentication_classes = [MicroserviceAuthentication]
     permission_classes = [IsAuthenticated]
     queryset = Order.objects.all()
     serializer_class = OrderSerializer

     def create(self, request, *args, **kwargs):
          serializer = self.serializer_class(data=request.data, context={"request": request})
          if serializer.is_valid():
               serializer.save()
               return Response(serializer.data, status=status.HTTP_200_OK)
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

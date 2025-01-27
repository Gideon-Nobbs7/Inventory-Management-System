from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import   ProductSerializer
from .models import Product
# Create your views here.


class ProductView(viewsets.ViewSet):
    def list(self, request):
        products = Product.objects.all()
        serializer =  ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer =  ProductSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ProductDetailView(viewsets.ViewSet):
    def get_product(self, id):
        product = Product.objects.get(id=id)
        return product
    
    def retrieve(self, request, id):
        data = self.get_product(id)
        serializer = ProductSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, id):
        data = self.get_product(id)
        serializer = ProductSerializer(instance=data, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, id):
        data = self.get_product(id)
        data.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

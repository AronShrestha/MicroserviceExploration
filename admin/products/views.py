from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product, User
from .serializers import ProductSerialzier
import random
from .producer import publish

# Create your views here.

class ProductViewSet(viewsets.ViewSet):
    def get_list(self, request):
        product = Product.objects.all()
        serializer = ProductSerialzier(product, many = True)
        
        return Response(serializer.data)
    
    def create(self, request):
        serializer = ProductSerialzier(data = request.data)
        serializer.is_valid(raise_exception=True)
        
        serializer.save()
        publish('product_created', serializer.data)
        return Response(serializer.data, status = status.HTTP_201_CREATED)
    
    def retrive(self, request, pk=None):
        product = Product.objects.get(id = pk)
        serializer = ProductSerialzier(product)
        return Response(serializer.data)
    
    
    def update(self, request, pk=None):
        product = Product.objects.get(id = pk)
        serializer = ProductSerialzier(instance = product, data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish('product_updated', serializer.data)
        return Response(serializer.data, status = status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk = None):
        product = Product.objects.get(id = pk)
        product.delete()
        publish('product_deleted', pk)
        return Response(status = status.HTTP_204_NO_CONTENT)
        


class UserAPIView(APIView):
    def get(self, _):
        
        user = User.objects.all()
        user = random.choice(user)
        return Response(
            {
                'id':user.id
            }
        )

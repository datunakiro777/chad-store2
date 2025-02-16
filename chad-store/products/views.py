from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from django.shortcuts import get_object_or_404
from products.models import Product, Review, Cart, FavoritedProduct, ProductTag
from products.serializers import ProductSerializer, CartSerializer, Product_Tag_Serializer, FavoritedProductSerializer
from rest_framework.views import APIView

@api_view(['GET', 'POST'])
def product_view(request):
    if request.method == 'GET':
        products = Product.objects.all()
        product_list = []
        
        for product in products:
            product_data = {
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'currency': product.currency,
            }
            product_list.append(product_data)

        return Response({'products': product_list})
    elif request.method == "POST":
        data = request.data
        serializer = ProductSerializer(data)
        if serializer.is_valid():
            new_product = Product.objects.create(
                name=data.get('name'),
                description=data.get('description'),
                price=data.get('price'),
                currency=data.get('currency', 'GEL'),
                quantity = data.get('quantity')
            )
            return Response({'id': new_product.id}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductTagViewSet(GenericAPIView, ListModelMixin, CreateModelMixin):
    queryset = ProductTag.objects.all()
    serializer_class = Product_Tag_Serializer
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
        

class FavoritedProductViewSet(GenericAPIView, ListModelMixin, CreateModelMixin):
    queryset = FavoritedProduct.objects.all()
    serializer_class = FavoritedProductSerializer
    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CartViewSet(GenericAPIView, CreateModelMixin, ListModelMixin):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_queryset(self):
        queryset = Cart.objects.filter(user=self.request.user)
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        if Cart.objects.filter(user=request.user).exists():
            return self.create(request, *args, **kwargs)
        else:
            pass
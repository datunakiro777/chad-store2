from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from products.models import Product, Review, Cart
from products.serializers import ProductSerializer, CartSerializer, Product_Tag_Serializer


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
        

@api_view(['GET', 'POST'])
def cart_view(request):
    if request.method == 'GET':
        cart_products = Cart.objects.get(user=request.user)
        cart_product_list = []
        for cart_product in cart_products:
            cart_poducts_data = {
                'products' : cart_product.products
            }
            cart_product_list.append(cart_poducts_data)
        return Response({'cart_products' : cart_poducts_data})
    elif request.method == 'POST':
        data = request.data
        serializer = CartSerializer(data)
        if serializer.is_valid():
            new_cart_products = Cart.products.add(
                product_id = data.get('product_id')
            )
            return Response({'products': new_cart_products}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def product_tag_view(request):
    if request.method == 'GET':
        products = Product.objects.all()
        product_tags_list = []
        for product in products:
            product_tag = {
                'name' : product.name,
                'tags' : product.product_tags            
            }
            product_tags_list.append(product_tag)
        return Response({'product_tags' : product_tags_list})
    elif request.method == 'POST':
        data = request.data
        serializer = Product_Tag_Serializer(data)
        if serializer.is_valid():
            product = Product.objects.get(id=data.get('product_id'))
            new_product_tags = product.product_tags.add(
                tag = data.get('tag')
            )
            return Response({'product_tags' : new_product_tags}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
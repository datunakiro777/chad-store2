from rest_framework import serializers
from products.models import Review, Product


class ProductSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.FloatField()
    currency = serializers.ChoiceField(choices=['GEL', 'USD', 'EUR'])

class CartSerializer(serializers.Serializer):
    Product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    def validate_product_id(self, value):
        try:
            Product.objects.get(id=value)
        except Product.DoesNotExist:
            raise serializers.ValidationError('product dose not exsist')
        return value
    
    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError('out of stock')
        return value
    

class Product_Tag_Serializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    tag = serializers.CharField()

    def validate_product_id(Self, value):
        try:
            Product.objects.get(id=value)
        except Product.DoesNotExist:
            raise serializers.ValidationError('product dose not exsist')
        return value
    
    def validate_tag(self, value):
        id = self.product_id
        product = Product.objects.filter(id=id)
        if product.filter(product_tags__iexact=value):
            raise serializers.ValidationError('tag is already in product')
        return value
from rest_framework import serializers
from products.models import Review, Product, ProductTag, FavoritedProduct, Cart


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
    
    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError('out of stock')
        return value
    

class Product_Tag_Serializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTag
        fields = '__all__'
    
    
    def validate_tag(self, value):
        id = self.product_id
        product = Product.objects.filter(id=id)
        if product.filter(product_tags__iexact=value):
            raise serializers.ValidationError('tag is already in product')
        return value
    

class FavoritedProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoritedProduct
        fields = "__all__"
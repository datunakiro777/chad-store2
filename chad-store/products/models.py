from django.db import models
from config.model_utils.models import TimeStampedModel
from products.choices import Currency
from django.core.validators import MaxValueValidator

class Product(TimeStampedModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField()
    currency = models.CharField(max_length=255, choices=Currency.choices, default=Currency.GEL)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.name
    
class Review(TimeStampedModel):
    user = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='reviews')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField()
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(5)])

    def __str__(self):
        return self.user
    
class ProductTag(TimeStampedModel):
    name = models.CharField(max_length=255)
    products = models.ManyToManyField('products.Product', related_name='product_tags')
    def __str__(self):
        return self.name
    

class Cart(TimeStampedModel, models.Model):
    products = models.ManyToManyField('products.Product', related_name='carts')
    user = models.OneToOneField('users.User', on_delete=models.SET_NULL, null=True, blank=True)


class ProductImage(TimeStampedModel, models.Model):
    image = models.ImageField(upload_to='products/')
    product = models.ForeignKey('products.Product', related_name='images', on_delete=models.CASCADE)

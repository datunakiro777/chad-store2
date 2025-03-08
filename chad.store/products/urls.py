from django.urls import path, include
from products.views import ProductViewSet, ReviewViewSet, FavoriteProductViewSet, CartViewSet, TagList, ProductImageViewSet
from rest_framework_nested import routers
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('products', ProductViewSet)
router.register('favorited_products', FavoriteProductViewSet)
router.register('cart', CartViewSet)
router.register('tags', TagList)
router.register('reviews', ReviewViewSet)

products_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_router.register('images', ProductImageViewSet, basename='product-images')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(products_router.urls))
]

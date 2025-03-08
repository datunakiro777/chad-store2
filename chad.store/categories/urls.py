from django.urls import path, include
from categories.views import CategoryListView, CategoryDetailView, CategoryImageViewSet
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

router = DefaultRouter()
router.register('categories', CategoryListView)

category_router = routers.NestedDefaultRouter(router, 'categories', lookup='category_images')
category_router.register('images', CategoryImageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include(category_router.urls))
]

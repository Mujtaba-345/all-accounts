from django.urls import path
from .views import BrandView, ShopView, BrandDeleteView, ShopDeleteView,LagerView,LagerDeleteView,ShopDetailView

urlpatterns = [
    path("brands/", BrandView.as_view(), name='brands'),
    path('brands/delete/<int:pk>', BrandDeleteView.as_view(), name='delete_brand'),
    path('brands/detail/<int:pk>/', BrandView.as_view(), name='brand_detail'),
    path("shop/", ShopView.as_view(), name='shop'),
    path('shop/delete/<int:pk>', ShopDeleteView.as_view(), name='delete_shop'),
    path('shop/detail/<int:pk>/', ShopView.as_view(), name='shop_detail'),
    path('lager/', LagerView.as_view(), name='lager'),
    path('lager/detail/<int:pk>/', LagerView.as_view(), name='lager_detail'),
    path('lager/delete/<int:pk>', LagerDeleteView.as_view(), name='delete_lager'),
    path('shop/<int:pk>/', ShopDetailView.as_view(), name='detail_shop'),

]

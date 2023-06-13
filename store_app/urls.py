from django.urls import path
from . import views




urlpatterns = [
    path('',views.index,name='index'),
    path('filter_brand/<int:id>/',views.filter_brand,name='filter_brand'),
    path('filter_phone/<int:id>/',views.filter_phone,name='filter_phone'),
    path('spaceautocomplete/', views.spaceautocomplete, name='spaceautocomplete'),
    path('search/', views.search, name='search'),
    path('product_inner_page/<int:id>/', views.product_inner_page, name='product_inner_page'),


    
    
    


]

from django.urls import path

from . import views


urlpatterns = [
    
    path('', views.CategoryList.as_view(), name='category_list'),
    path('<int:category_id>', views.CategoryDetail.as_view(), name='category_detail'),
    path('subcategory', views.SubCategoryList.as_view(), name='subcategory_list'),
    path('subcategory/<int:subcategory_id>', views.SubCategoryDetail.as_view(), name='subcategory_detail'),
]

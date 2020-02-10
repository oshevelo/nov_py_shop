from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination



from .models import Category
from .models import SubCategory
from .serializers import SubCategorySerializer
from .serializers import CategorySerializer

class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination

    
class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
       
    def get_object(self):
        obj = get_object_or_404(Category, pk=self.kwargs.get('category_id'))
        return obj

class SubCategoryList(generics.ListCreateAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    pagination_class = LimitOffsetPagination


class SubCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SubCategorySerializer
       
    def get_object(self):
        obj = get_object_or_404(SubCategory, pk=self.kwargs.get('subcategory_id'))
        return obj    

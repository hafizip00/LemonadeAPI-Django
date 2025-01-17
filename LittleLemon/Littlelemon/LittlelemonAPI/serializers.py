from rest_framework import serializers
from .models import MenuItem, Category
from decimal import Decimal

# class MenuItemSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = MenuItem
#         fields = ["id","title", "price", "inventory"]

# class MenuItemSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length = 255)
#     price = serializers.DecimalField(max_digits = 6 , decimal_places=2)
#     inventory = serializers.IntegerField()


class MenuCategorySerailizer(serializers.ModelSerializer):
    slug = serializers.SlugField()
    title = serializers.CharField(max_length = 255)
    class Meta:
        model = Category
        fields = ['id' , 'slug' , 'title']

class MenuItemSerializer(serializers.ModelSerializer):
    stock = serializers.IntegerField(source='inventory')
    price_after_tax = serializers.SerializerMethodField(method_name='after_tax')
    category = MenuCategorySerailizer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price' , 'stock' , 'price_after_tax', 'category' , 'category_id'] 

    
    def after_tax(self , product:MenuItem):
        return product.price * Decimal(1.1)
    

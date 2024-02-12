from rest_framework import serializers

from rest_api.models import Category, Tags, Stock, TagMap, Quantity

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']

class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ['name']

class StocksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['sku', 'name', 'price', 'category']

class TagMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagMap
        fields = ['tag', 'sku']

class QuantitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Quantity
        fields = ['sku', 'allocated', 'alloc_build', 'alloc_sales', 'available', 'incoming', 'build_order', 'net_stock', 'can_build', 'instock']
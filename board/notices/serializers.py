from rest_framework import serializers
from .models import Notice, Category

# category model serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

# notices model serializer
class NoticeSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    class Meta:
        model = Notice
        fields = '__all__'
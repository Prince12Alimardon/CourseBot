from rest_framework import serializers
from .models import Course, Book, Info


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class InfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Info
        fields = '__all__'

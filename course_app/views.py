from rest_framework import generics
from .models import Course, Book, Info
from .serializers import CourseSerializer, BookSerializer, InfoSerializer


class CourseList(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseDetail(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookDetail(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class InfoDetail(generics.ListAPIView):
    queryset = Info.objects.all()
    serializer_class = InfoSerializer

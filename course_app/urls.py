from django.urls import path
from .views import CourseList, CourseDetail, BookList, BookDetail, InfoDetail

urlpatterns = [
    path('courses/', CourseList.as_view(), name='course-list'),
    path('courses/<int:pk>/', CourseDetail.as_view(), name='course-detail'),
    path('books/', BookList.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetail.as_view(), name='book-detail'),
    path('info/', InfoDetail.as_view(), name='info-detail'),
]

from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='courses/')

    def __str__(self):
        return self.title


class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    pdf = models.FileField(upload_to='books/')
    image = models.ImageField(upload_to='books/')

    def __str__(self):
        return self.title


class Info(models.Model):
    address = models.CharField(max_length=255)
    link = models.URLField()
    phone = models.CharField(max_length=20)
    image = models.ImageField(upload_to='info/')

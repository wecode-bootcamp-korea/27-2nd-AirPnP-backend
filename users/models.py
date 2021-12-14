from django.db import models

from categories.models import Category

class User(models.Model): 
    name       = models.CharField(max_length=45)
    email      = models.EmailField(unique=True)
    kakao_id   = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta: 
        db_table = 'uesrs'

class Host(models.Model): 
    phone_number = models.CharField(max_length=45, unique=True)
    carrer       = models.IntegerField()
    price        = models.IntegerField()
    description  = models.TextField()
    longitude    = models.DecimalField(max_digits=9, decimal_places=6)
    latitude     = models.DecimalField(max_digits=9, decimal_places=6)
    category     = models.ForeignKey(Category, on_delete=models.CASCADE)
    user         = models.ForeignKey('User', on_delete=models.CASCADE)
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta: 
        db_table = 'hosts'

class Image(models.Model): 
    image_url = models.TextField()
    host      = models.ForeignKey('Host', on_delete=models.CASCADE)

    class Meta: 
        db_table = 'images'

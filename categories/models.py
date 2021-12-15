from django.db import models

class Category(models.Model): 
    talent     = models.CharField(max_length=45)
    
    class Meta: 
        db_table = 'categories'

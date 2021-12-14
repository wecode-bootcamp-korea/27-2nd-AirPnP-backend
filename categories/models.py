from django.db import models

class Category(models.Model): 
    talant     = models.CharField(max_length=45)
    
    class Meta: 
        db_table = 'categories'

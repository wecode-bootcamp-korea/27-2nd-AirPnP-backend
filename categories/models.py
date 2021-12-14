from django.db import models

class Category(models.Model): 
    talant     = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta: 
        db_table = 'categories'

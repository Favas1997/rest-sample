from django.db import models

# Create your models here.
class product(models.Model):
    id = models.AutoField(primary_key=True)
    name=models.CharField(max_length=30)
    description=models.CharField(max_length=120)
    price=models.IntegerField(max_length=4)
    sale_start=models.DateField()
    sale_end=models.DateField()

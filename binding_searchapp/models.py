# Import necessary modules

from django.db import models
from django.urls import  reverse


class Booktype(models.Model):
    btype = models.CharField(max_length=100, unique=True)
    class Meta:
        ordering=('btype',)


# Create model gor book
class Book(models.Model):
    binding_name = models.CharField(max_length=150)
    author_name = models.CharField(max_length=150)
    type = models.ForeignKey(Booktype, on_delete=models.CASCADE)
    price = models.FloatField()
    publication = models.CharField(max_length=100)

    class Meta:
        ordering=('binding_name',)
    def __str__(self):
        return self.binding_name

    def get_url(self):
       return reverse('binding_detail', args=[self.id])

BINDING_MODEL_TYPES = [
    ('m1', 'Unspecified'),
    ('m2', 'Tutorial'),
    ('m3', 'Research'),
    ('m4', 'Review'),
]


class Binding(models.Model):
    drug = models.TextField()
    target = models.TextField()

    gcnnet_bindingdb_ic50 = models.FloatField()
    gcnnet_bdtdc_ic50 = models.FloatField()
    model = models.CharField(max_length=100)
    type = models.CharField(max_length=2, choices=BINDING_MODEL_TYPES, default='m1')

    class Meta:
        ordering=('drug',)
    def __str__(self):
        return self.drug

    def get_binding_details(self):
       return reverse('binding_detail', args=[self.id])
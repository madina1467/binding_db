# Import necessary modules

from django.db import models
# from django import models
# from django_rdkit import models
# from django_rdkit.models import *
from django.contrib.postgres.fields import ArrayField
from django import forms
from django.urls import reverse

BINDING_MODEL_TYPES = [
    ('m1', 'bdtdc_ki_shrinked_test'),
    ('m2', 'bdtdc_kd_shrinked_test'),
    ('m3', 'bdtdc_ic50_shrinked_test'),
]

class Binding(models.Model):
    drug = models.TextField()
    target = models.TextField()

    gcnnet_bindingdb_ic50 = models.FloatField()
    gcnnet_bdtdc_ic50 = models.FloatField()
    model = models.CharField(max_length=100)

    # type = models.CharField(max_length=2, choices=BINDING_MODEL_TYPES, default='m1')
    #
    # def type_to_string(self):
    #     if self.type == 'm1':
    #         return 'bdtdc_ki_shrinked_test'
    #     elif self.type == 'm2':
    #         return 'bdtdc_kd_shrinked_test'
    #     elif self.type == 'm3':
    #         return 'bdtdc_ic50_shrinked_test'

    class Meta:
        ordering = ('drug',)

    def __str__(self):
        return self.drug

    def get_binding_details(self):
        return reverse('binding_detail', args=[self.id])


class BindingForm(forms.ModelForm):
    class Meta:
        model = Binding
        fields = (
            'drug', 'target', 'gcnnet_bindingdb_ic50', 'gcnnet_bdtdc_ic50', 'model'
        )


# class Entry(models.Model):
#     m1 = ArrayField(
#         model_container=Binding,
#         model_form_class=BindingForm)
#
#     m2 = ArrayField(
#         model_container=Binding,
#         model_form_class=BindingForm)
#
#     m3 = ArrayField(
#         model_container=Binding,
#         model_form_class=BindingForm)

    # objects = models.DjongoManager()

# class BindingModels(models.Model):
#     m1 = models.ForeignKey(Binding) # = JSONField()
#     m2 = models.ForeignKey(Binding)
#     m3 = models.ArrayField(models.ArrayField(Binding))

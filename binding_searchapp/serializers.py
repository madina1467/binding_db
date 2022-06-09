from rest_framework import serializers

from binding_searchapp.models import Binding


class BindingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Binding
        fields = '__all__'
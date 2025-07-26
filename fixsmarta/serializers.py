from rest_framework import serializers
from .models import *



class Register(serializers.ModelSerializer):
    class Meta:
        model = SmartFix
        fields = '__all__'

    def validate(self, data):
        exclude_fields = ['password', 'image']  # Adjust as per your model
        for field, value in data.items():
            if field not in exclude_fields and isinstance(value, str):
                data[field] = value.lower()
        return data


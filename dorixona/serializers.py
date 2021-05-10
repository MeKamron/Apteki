from rest_framework import serializers
from .models import *

class ViloyatSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('nomi',)
        model = Viloyat

class TumanSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('nomi', 'viloyat')
        model = Tuman


class DorixonaSerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField('get_image_url')

    class Meta:
        model = Dorixona    
        fields = ('nomi', 'yuridik_nomi', 'logo', 'logo_url','ish_24_soat',
            'manzil', 'tuman', 'telfon', 'xolati', 'uzunlik', 'kenglik',
            'map_url', 'qoshilgan', 'yangilangan')
    
    def get_image_url(self, obj):
        return obj.logo.url


class DoriSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('nomi', 'nomi', 'dorixona')
        model = Dori
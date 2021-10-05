from django.contrib.auth.models import User
from django.db import models
from rest_framework.validators import UniqueValidator
from api.models import Autor, Genero, Libro
from rest_framework import serializers, viewsets, routers
from django.contrib.auth import password_validation

class GeneroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genero
        fields = ['id','nombre', 'descripcion']


class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = ['id','nombre','apellido_paterno','apellido_materno','f_nacimiento']


class LibroSerializer(serializers.ModelSerializer):
    autor = AutorSerializer(many=False, read_only=True)
    genero = GeneroSerializer(many=True, read_only=True)
    # idautor = serializers.IntegerField(required=False)
    # generoId = serializers.IntegerField(required=False)

    class Meta:
        model = Libro
        fields = ['id','titulo','f_publicacion','descripcion','autor','genero']

class LibroSerializerCreate(serializers.ModelSerializer):
    autor = serializers.PrimaryKeyRelatedField(queryset=Autor.objects.all(), many=False) 
    genero = serializers.PrimaryKeyRelatedField(queryset=Genero.objects.all(), many=True) 

    class Meta:
        model = Libro
        fields = ['titulo','f_publicacion','descripcion','autor','genero']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','password'] 

class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):

        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user
    class Meta:
        model = User
        fields = ['username','password','email','first_name','last_name'] 
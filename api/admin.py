from django.contrib import admin
from api import models

# Register your models here.

admin.site.register(models.Autor)
admin.site.register(models.Genero)
admin.site.register(models.Libro)
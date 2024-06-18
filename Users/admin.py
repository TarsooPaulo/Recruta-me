from django.contrib import admin
from Users import models

# Register your models here.

@admin.register(models.Profile)
class teste_admin(admin.ModelAdmin):
    ...
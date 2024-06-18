from django.contrib import admin
from teste import models

# Register your models here.

@admin.register(models.foo)
class teste_admin(admin.ModelAdmin):
    ...
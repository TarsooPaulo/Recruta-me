from typing import Optional
from django.db import models
from PIL import Image
from django.http import HttpResponse
from django.core.exceptions import ValidationError
import os
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver

class foo(models.Model):
    first_name = models.CharField("First Name", max_length=50,)
    last_name = models.CharField("Last Name", max_length=50, blank=True)
    age = models.IntegerField("Age", default=0)
    cargo = models.CharField(("cargo"), max_length=50,)
    email = models.EmailField("E-mail", max_length=254)
    phone = models.CharField("Phone", max_length=50, blank=True)
    description = models.TextField("Description")
    photo = models.ImageField("Photo", upload_to="pictures/%Y/%m", blank=True,)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.redimensionar_imagem()

    def delete(self, *args, **kwargs):
        if self.photo:
            if os.path.isfile(self.photo.path):
                os.remove(self.photo.path)
        super().delete(*args, **kwargs)

    def redimensionar_imagem(self):
        if self.photo:
            img = Image.open(self.photo.path)
            print(img.height)
            if img.height <= 300 or img.height <=500:
                new_img = img.resize(size=(300, 275))
                new_img.save(
                self.photo.path,
                optimize=True,
                quality=70,
                )
            elif img.height > 500:                
                new_img = img.resize(size=(300, 400))
                new_img.save(
                    self.photo.path,
                    optimize=True,
                    quality=70,
                    )
            else:
                return img
                
    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'

def delete_photo(photo_field):
    if photo_field:
        if os.path.isfile(photo_field.path):
            os.remove(photo_field.path)

def delete_photo_on_change(sender, instance, **kwargs):
    if instance.pk:
        original = sender.objects.get(pk=instance.pk)
        if original.photo != instance.photo:
            delete_photo(original.photo)

def delete_photo_on_delete(sender, instance, **kwargs):
    delete_photo(instance.photo)
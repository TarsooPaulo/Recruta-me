from django.db import models
import os
from PIL import Image
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default='')
    first_name = models.CharField(_("Nome"), max_length=50)
    last_name = models.CharField(_("Sobrenome"), max_length=50, blank=True)
    email = models.EmailField(null=True, blank=True)
    age = models.IntegerField(_("Idade"), default=0)
    cargo = models.CharField(_("Cargo"), max_length=50)
    phone = models.CharField(_("Telefone"), max_length=50, blank=True)
    description = models.TextField(_("Descrição"),blank=True)
    photo = models.ImageField(_("Foto"), upload_to="pictures/%Y/%m", blank=True, null=True)
    
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
            if img.height <= 500:
                new_img = img.resize(size=(300, 275))
                new_img.save(
                self.photo.path,
                optimize=True,
                quality=70,
                )
            else:                
                new_img = img.resize(size=(300, 400))
                new_img.save(
                    self.photo.path,
                    optimize=True,
                    quality=70,
                    )


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
# Generated by Django 4.2.3 on 2023-07-21 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teste', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='foo',
            name='campo_texto',
        ),
        migrations.AddField(
            model_name='foo',
            name='First_Name',
            field=models.CharField(blank=True, max_length=50, verbose_name='First Name'),
        ),
        migrations.AddField(
            model_name='foo',
            name='Last_Name',
            field=models.CharField(blank=True, max_length=50, verbose_name='Last_Name'),
        ),
        migrations.AddField(
            model_name='foo',
            name='Photo',
            field=models.ImageField(blank=True, upload_to='', verbose_name='Photo'),
        ),
        migrations.AddField(
            model_name='foo',
            name='age',
            field=models.IntegerField(default=0, verbose_name='age'),
        ),
        migrations.AddField(
            model_name='foo',
            name='description',
            field=models.TextField(blank=True, verbose_name='Description'),
        ),
        migrations.AddField(
            model_name='foo',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='E-mail'),
        ),
        migrations.AddField(
            model_name='foo',
            name='phone',
            field=models.CharField(blank=True, max_length=50, verbose_name='Phone'),
        ),
    ]

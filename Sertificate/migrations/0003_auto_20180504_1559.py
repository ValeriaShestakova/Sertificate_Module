# Generated by Django 2.0.3 on 2018-05-04 12:59

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sertificate', '0002_auto_20180504_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='teacher',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Преподаватель'),
        ),
    ]
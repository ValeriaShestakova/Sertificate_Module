from django.contrib import admin

from .models import Group, Certificate

admin.site.register(Certificate)
admin.site.register(Group)
from django.contrib import admin

from .models import Group, Certificate, Program, Task, Result

admin.site.register(Program)
admin.site.register(Certificate)
admin.site.register(Group)
admin.site.register(Task)
admin.site.register(Result)


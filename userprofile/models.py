
from django.db import models
from django.contrib.auth.models import User, Group


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(verbose_name='ФИО', max_length=300, null=True)
    status = models.CharField(verbose_name='Статус пользователя', max_length=100)  # student, teacher, secretary
    group = models.ForeignKey(Group, models.SET_NULL, null=True, verbose_name='Группа')

    def __unicode__(self):
        return self.user

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

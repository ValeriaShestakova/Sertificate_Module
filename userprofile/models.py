
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from Sertificate.models import Task, Group


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fullname = models.CharField(verbose_name='ФИО', max_length=300, null=True)
    status = models.CharField(verbose_name='Статус пользователя', max_length=100)  # student, teacher, secretary
    group = models.ForeignKey(Group, models.SET_NULL, null=True, verbose_name='Группа')
    task = models.ManyToManyField(Task, verbose_name='Решенные задания', null=True)

    def __unicode__(self):
        return self.user

    def to_rus(self):
        if self.status == 'teacher':
            return 'преподаватель'
        elif self.status == 'student':
            return 'обучающийся'
        elif self.status == 'secretary':
            return 'секретарь'
        elif self.status == 'admin':
            return 'администратор'
        else:
            return ' '

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()

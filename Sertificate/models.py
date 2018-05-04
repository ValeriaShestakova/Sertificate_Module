from django.db import models
from django.contrib.auth.models import User


class Group(models.Model):
    program_name = models.CharField(verbose_name='Название программы', max_length=200)
    group_name = models.CharField(verbose_name='Номер группы', max_length=100)
    begin_date = models.DateTimeField(verbose_name='Дата начала курса')
    end_date = models.DateTimeField(verbose_name='Дата окончания курса')
    teacher = models.ManyToManyField(User, verbose_name='Преподаватель')

    def __str__(self):
        return self.group_name

    class Meta:
        verbose_name = 'группа'
        verbose_name_plural = 'группы'


class Certificate(models.Model):
    program_name = models.CharField(verbose_name='Название программы', max_length=200)
    certificate_number = models.CharField(verbose_name='Номер', max_length=200)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(verbose_name='Статус сертификата', max_length=200)  # not_issued, required, issued

    def __str__(self):
        return self.certificate_number

    class Meta:
        verbose_name = 'сертификат'
        verbose_name_plural = 'сертификаты'





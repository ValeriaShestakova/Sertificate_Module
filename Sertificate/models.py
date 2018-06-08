from django.db import models
from django.contrib.auth.models import User


class Program(models.Model):
    program_name = models.CharField(verbose_name='Название программы', max_length=200)
    num_hours = models.IntegerField(verbose_name='Количество часов', default=1)

    def __str__(self):
        return self.program_name

    class Meta:
        verbose_name = 'программа'
        verbose_name_plural = 'программы'


class Task(models.Model):
    task_title = models.CharField(verbose_name='Задание', max_length=200)
    task_num = models.IntegerField(verbose_name='Номер задания', default=1)
    program = models.ForeignKey(Program, models.SET_NULL, null=True, default=1, verbose_name='Программа обучения')

    def __str__(self):
        return self.task_title

    class Meta:
        verbose_name = 'задание'
        verbose_name_plural = 'задания'


class Group(models.Model):
    group_number = models.CharField(verbose_name='Номер группы', max_length=100)
    begin_date = models.DateField(verbose_name='Дата начала курса')
    end_date = models.DateField(verbose_name='Дата окончания курса')
    program = models.ForeignKey(Program, models.SET_NULL, default=1, null=True, verbose_name='Программа обучения')
    teacher = models.ManyToManyField(User, verbose_name='Преподаватель')

    def __str__(self):
        return self.group_number

    class Meta:
        verbose_name = 'группа'
        verbose_name_plural = 'группы'


class Certificate(models.Model):
    certificate_number = models.CharField(verbose_name='Номер', max_length=200)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, models.SET_NULL, default=1, null=True, verbose_name='Программа обучения')
    status = models.CharField(verbose_name='Статус сертификата', max_length=200, default='create')  # not_issued, issued, create
    pay = models.BooleanField(verbose_name='Произведена оплата', default=False)
    docs = models.BooleanField(verbose_name='Сданы документы', default=False)
    change = models.BooleanField(verbose_name='Возможны ли изменения', default=True) #true - сертификат не выдавался, изменения возможны
    hash = models.CharField(verbose_name='Хеш-код', max_length=500, default='')

    def __str__(self):
        return self.certificate_number

    class Meta:
        verbose_name = 'сертификат'
        verbose_name_plural = 'сертификаты'


class Result(models.Model):
    certificate = models.OneToOneField(Certificate, on_delete=models.CASCADE)
    student = models.ForeignKey(User, models.SET_NULL, default=1, null=True, blank=True, verbose_name='Обучающийся')
    task = models.ManyToManyField(Task, verbose_name='Выполненные задания', blank=True)
    approved = models.BooleanField(verbose_name='Выполнены необходимые задания', default=False)

    def __str__(self):
        return self.student.userprofile.fullname

    class Meta:
        verbose_name = 'результат'
        verbose_name_plural = 'результаты'



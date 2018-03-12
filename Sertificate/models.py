from django.db import models

class Group(models.Model):
    program_name = models.CharField(verbose_name='Название программы', max_length=200)
    group_name = models.CharField(verbose_name='Номер группы', max_length=100)
    begin_date = models.DateTimeField(verbose_name='Дата начала курса')
    end_date = models.DateTimeField(verbose_name='Дата окончания курса')
    def __str__(self):
        return self.group_name
    class Meta:
        verbose_name = 'группа'
        verbose_name_plural = 'группы'

class Teacher(models.Model):
    teacher_name = models.TextField(verbose_name='ФИО', max_length=500)
    login = models.CharField(verbose_name="Логин", max_length=100, unique=True, null=False)
    password = models.CharField(verbose_name="Пароль", max_length=100, unique=True, null=False)
    group = models.ManyToManyField(Group)
    def __str__(self):
        return self.teacher_name
    class Meta:
        verbose_name = 'преподаватель'
        verbose_name_plural = 'преподаватели'

class Student(models.Model):
    student_name = models.TextField(verbose_name='ФИО', max_length=500)
    login = models.CharField(verbose_name="Логин", max_length=100, unique=True, null=False)
    password = models.CharField(verbose_name="Пароль", max_length=100, unique=True, null=False)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.student_name
    class Meta:
        verbose_name = 'обучающийся'
        verbose_name_plural = 'обучающиеся'

class Certificate(models.Model):
    program_name = models.CharField(verbose_name='Название программы', max_length=200)
    certificate_number = models.CharField(verbose_name='Номер', max_length=200)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    status = models.CharField(verbose_name='Статус сертификата', max_length=200) #not_issued, required, issued
    def __str__(self):
        return self.certificate_number
    class Meta:
        verbose_name = 'сертификат'
        verbose_name_plural = 'сертификаты'





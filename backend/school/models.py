from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from school import SectionActionStatus, Regions


class School(models.Model):
    """ Модель школы """

    logo = models.ImageField(upload_to='school/logo/', null=True, blank=True)
    name = models.CharField(max_length=155)
    address = models.CharField(max_length=155)
    direct = models.CharField(max_length=155)
    language = models.CharField(max_length=155)
    country = models.CharField(max_length=155, null=True, blank=True)
    region = models.CharField(max_length=155, choices=Regions.choices, null=False)
    city = models.CharField(max_length=155, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    bin = models.CharField(max_length=12)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Школа')
        verbose_name_plural = _('Школы')
        db_table = 'school'


class SchoolRequisites(models.Model):
    """ Модель реквизитов школы """

    school = models.ForeignKey(School, on_delete=models.CASCADE, null=False)
    bank_name = models.CharField(max_length=155, null=False)
    bank_address = models.CharField(max_length=155, null=False)
    bank_bik = models.CharField(max_length=9, null=False)
    bank_iik = models.CharField(max_length=20, null=False)
    bank_kbe = models.CharField(max_length=20, null=False)
    bank_bin = models.CharField(max_length=12, null=False)

    def __str__(self):
        return f'{self.school} - {self.bank_name}'

    class Meta:
        verbose_name = _('Реквизит школы')
        verbose_name_plural = _('Реквизиты школ')
        db_table = 'school_requisites'


class Class(models.Model):
    """ Модель класса """

    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True)
    class_num = models.IntegerField(null=False)
    class_liter = models.CharField(max_length=10, null=False)
    description = models.TextField(null=True, blank=True)
    mentor = models.ForeignKey('authorization.User', on_delete=models.SET_NULL, null=True, related_name='class_teacher')
    is_graduated = models.BooleanField(default=False)
    max_class_num = models.PositiveIntegerField(default=11)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.class_num}{self.class_liter}'

    class Meta:
        verbose_name = _('Класс')
        verbose_name_plural = _('Классы')
        db_table = 'class'


class OurSchools(models.Model):
    """ Модель наших школ """

    school = models.OneToOneField(School, on_delete=models.SET_NULL, null=True)
    city_short_name = models.CharField(max_length=155, null=False)
    short_name = models.CharField(max_length=155, null=False)
    fix_sum_contract = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    is_yearly_payment = models.BooleanField(default=True)

    def __str__(self):
        return self.short_name

    class Meta:
        verbose_name = _("Информация о школе")
        verbose_name_plural = _("Информация о школах")
        db_table = 'our_schools'


class Subject(models.Model):
    """ Модель курса """

    classroom = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=155, null=False)
    teacher = models.ForeignKey('authorization.User', on_delete=models.SET_NULL, null=True, related_name='subject_teacher')
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Предмет')
        verbose_name_plural = _('Предметы')
        db_table = 'subject'


class SubjectSection(models.Model):
    """ Модель раздела курса """

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=False, db_column='subject')
    datetime = models.DateTimeField(null=False)
    duration = models.PositiveSmallIntegerField(default=1)
    cabinet = models.CharField(max_length=155, null=False)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.subject} - {self.datetime}'

    class Meta:
        verbose_name = _('Раздел предмета')
        verbose_name_plural = _('Разделы предметов')
        db_table = 'subject_section'


class SectionAction(models.Model):
    """ Модель действия раздела """

    section = models.ForeignKey(SubjectSection, on_delete=models.CASCADE, null=False)
    student = models.ForeignKey('authorization.Student', on_delete=models.CASCADE, null=False)
    status = models.CharField(max_length=155, choices=SectionActionStatus.choices, default=SectionActionStatus.ATTENDED)
    datetime = models.DateTimeField(auto_now_add=True)
    grade = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.section} - {self.student}'

    class Meta:
        verbose_name = _('Посещение раздела')
        verbose_name_plural = _('Посещения разделов')
        db_table = 'section_attendance'


class SectionHomework(models.Model):
    """ Модель домашнего задания раздела """

    section = models.ForeignKey(SubjectSection, on_delete=models.CASCADE, null=False)
    files = models.FileField(upload_to='homework/', null=True, blank=True)
    datetime = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=False)
    deadline = models.DateTimeField(null=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.section} - {self.deadline}'

    class Meta:
        verbose_name = _('Домашнее задание')
        verbose_name_plural = _('Домашние задания')
        db_table = 'section_homework'


class SectionHomeworkAnswer(models.Model):
    """ Модель ответа на домашнее задание """

    homework = models.ForeignKey(SectionHomework, on_delete=models.CASCADE, null=False)
    student = models.ForeignKey('authorization.Student', on_delete=models.CASCADE, null=False)
    files = models.FileField(upload_to='homework/answers/', null=True, blank=True)
    datetime = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=False)

    def __str__(self):
        return f'{self.homework} - {self.student}'

    class Meta:
        verbose_name = _('Ответ на домашнее задание')
        verbose_name_plural = _('Ответы на домашние задания')
        db_table = 'section_homework_answer'


class SectionHomeworkGrade(models.Model):
    """ Модель оценки домашнего задания """

    homework = models.ForeignKey(SectionHomework, on_delete=models.CASCADE, null=False)
    student = models.ForeignKey('authorization.Student', on_delete=models.CASCADE, null=False)
    grade = models.PositiveSmallIntegerField(null=False)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.homework} - {self.student}'

    class Meta:
        verbose_name = _('Оценка домашнего задания')
        verbose_name_plural = _('Оценки домашних заданий')
        db_table = 'section_homework_grade'


class SectionTests(models.Model):
    """ Модель тестов раздела """

    section = models.ForeignKey(SubjectSection, on_delete=models.CASCADE, null=False)
    files = models.FileField(upload_to='tests/', null=True, blank=True)
    datetime = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=False)
    deadline = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.section} - {self.deadline}'

    class Meta:
        verbose_name = _('Тест')
        verbose_name_plural = _('Тесты')
        db_table = 'section_tests'


class SectionTestsAnswer(models.Model):
    """ Модель ответа на тест """

    test = models.ForeignKey(SectionTests, on_delete=models.CASCADE, null=False)
    student = models.ForeignKey('authorization.Student', on_delete=models.CASCADE, null=False)
    files = models.FileField(upload_to='tests/answers/', null=True, blank=True)
    datetime = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=False)

    def __str__(self):
        return f'{self.test} - {self.student}'

    class Meta:
        verbose_name = _('Ответ на тест')
        verbose_name_plural = _('Ответы на тесты')
        db_table = 'section_tests_answer'


class SectionTestsGrade(models.Model):
    """ Модель оценки теста """

    test = models.ForeignKey(SectionTests, on_delete=models.CASCADE, null=False)
    student = models.ForeignKey('authorization.Student', on_delete=models.CASCADE, null=False)
    grade = models.PositiveSmallIntegerField(null=False)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.test} - {self.student}'

    class Meta:
        verbose_name = _('Оценка теста')
        verbose_name_plural = _('Оценки тестов')
        db_table = 'section_tests_grade'

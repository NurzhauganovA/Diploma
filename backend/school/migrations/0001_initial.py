# Generated by Django 5.0.2 on 2024-04-02 20:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authorization', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='school/logo/')),
                ('name', models.CharField(max_length=155)),
                ('address', models.CharField(max_length=155)),
                ('direct', models.CharField(max_length=155)),
                ('language', models.CharField(max_length=155)),
                ('country', models.CharField(blank=True, max_length=155, null=True)),
                ('region', models.CharField(choices=[('Batys', 'Западно-Казахстанская область'), ('Aqtobe', 'Актюбинская область'), ('Atyrau', 'Атырауская область'), ('Mangystau', 'Мангистауская область'), ('Qostanay', 'Костанайская область'), ('Soltustik', 'Северо-Казахстанская область'), ('Pavlodar', 'Павлодарская область'), ('Qaragandy', 'Карагандинская область'), ('Ulytau', 'Улытауская область'), ('Qyzylorda', 'Кызылординская область'), ('Turkistan', 'Туркестанская область'), ('Zhambyl', 'Жамбылская область'), ('Almaty', 'Алматинская область'), ('Zhetisu', 'Жетысуская область'), ('Abay', 'Абайская область'), ('Shygys', 'Восточно-Казахстанская область'), ('Aqmola', 'Акмолинская область')], max_length=155)),
                ('city', models.CharField(blank=True, max_length=155, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('bin', models.CharField(max_length=12)),
            ],
            options={
                'verbose_name': 'Школа',
                'verbose_name_plural': 'Школы',
                'db_table': 'school',
            },
        ),
        migrations.CreateModel(
            name='OurSchools',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city_short_name', models.CharField(max_length=155)),
                ('short_name', models.CharField(max_length=155)),
                ('fix_sum_contract', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_yearly_payment', models.BooleanField(default=True)),
                ('school', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='school.school')),
            ],
            options={
                'verbose_name': 'Информация о школе',
                'verbose_name_plural': 'Информация о школах',
                'db_table': 'our_schools',
            },
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_num', models.IntegerField()),
                ('class_liter', models.CharField(max_length=10)),
                ('description', models.TextField(blank=True, null=True)),
                ('is_graduated', models.BooleanField(default=False)),
                ('max_class_num', models.PositiveIntegerField(default=11)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('mentor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='class_teacher', to=settings.AUTH_USER_MODEL)),
                ('school', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='school.school')),
            ],
            options={
                'verbose_name': 'Класс',
                'verbose_name_plural': 'Классы',
                'db_table': 'class',
            },
        ),
        migrations.CreateModel(
            name='SchoolRequisites',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_name', models.CharField(max_length=155)),
                ('bank_address', models.CharField(max_length=155)),
                ('bank_bik', models.CharField(max_length=9)),
                ('bank_iik', models.CharField(max_length=20)),
                ('bank_kbe', models.CharField(max_length=20)),
                ('bank_bin', models.CharField(max_length=12)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.school')),
            ],
            options={
                'verbose_name': 'Реквизит школы',
                'verbose_name_plural': 'Реквизиты школ',
                'db_table': 'school_requisites',
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=155)),
                ('description', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('classroom', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='school.class')),
                ('teacher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subject_teacher', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Прдемет',
                'verbose_name_plural': 'Предметы',
                'db_table': 'subject',
            },
        ),
        migrations.CreateModel(
            name='SubjectSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('duration', models.PositiveSmallIntegerField(default=1)),
                ('subject', models.ForeignKey(db_column='subject', on_delete=django.db.models.deletion.CASCADE, to='school.subject')),
            ],
            options={
                'verbose_name': 'Раздел предмета',
                'verbose_name_plural': 'Разделы предметов',
                'db_table': 'subject_section',
            },
        ),
        migrations.CreateModel(
            name='SectionAction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('ATTENDED', 'Посещено'), ('ABSENT', 'Отсутствие'), ('PERMITTED', 'Разрешено'), ('LATE', 'Опоздание'), ('LEFT', 'Покинул занятие')], default='ATTENDED', max_length=155)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('grade', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authorization.student')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.subjectsection')),
            ],
            options={
                'verbose_name': 'Посещение раздела',
                'verbose_name_plural': 'Посещения разделов',
                'db_table': 'section_attendance',
            },
        ),
    ]

# Generated by Django 5.0.2 on 2024-04-02 18:16

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authorization', '0004_student_stud_class_student_user'),
        ('school', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract_date', models.DateField()),
                ('contract_date_close', models.DateField(null=True)),
                ('name', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_type', models.CharField(choices=[('MONTHLY', 'Ежемесячно'), ('QUARTERLY', 'Ежеквартально'), ('ANNUAL', 'Ежегодно')], default='MONTHLY', max_length=255)),
                ('status', models.CharField(choices=[('FORMED', 'Сформирован'), ('CONSIDERATION', 'На рассмотрении'), ('SIGNED', 'Подписан'), ('FINISHED', 'Завершен'), ('CANCELED', 'Отменен'), ('DISSOLVED', 'Расторгнут')], default='FORMED', max_length=255)),
                ('final_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('edu_year', models.CharField(max_length=255)),
                ('classroom', models.ForeignKey(db_column='classroom', null=True, on_delete=django.db.models.deletion.SET_NULL, to='school.class')),
                ('school', models.ForeignKey(db_column='school', null=True, on_delete=django.db.models.deletion.SET_NULL, to='school.school')),
                ('student', models.ForeignKey(db_column='student', null=True, on_delete=django.db.models.deletion.SET_NULL, to='authorization.student')),
            ],
            options={
                'verbose_name': 'Контракт',
                'verbose_name_plural': 'Контракты',
                'db_table': 'contract',
            },
        ),
        migrations.CreateModel(
            name='ContractFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='contract/files/')),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('contract', models.ForeignKey(db_column='contract', null=True, on_delete=django.db.models.deletion.SET_NULL, to='contract.contract')),
            ],
            options={
                'verbose_name': 'Файл контракта',
                'verbose_name_plural': 'Файлы контрактов',
                'db_table': 'contract_file',
            },
        ),
        migrations.CreateModel(
            name='ContractMonthPay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.DateField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('contract', models.ForeignKey(db_column='contract', null=True, on_delete=django.db.models.deletion.SET_NULL, to='contract.contract')),
            ],
            options={
                'verbose_name': 'Ежемесячный платеж',
                'verbose_name_plural': 'Ежемесячные платежи',
                'db_table': 'contract_month_pay',
            },
        ),
        migrations.CreateModel(
            name='ContractDayPay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('contract_month', models.ForeignKey(db_column='contract_month', null=True, on_delete=django.db.models.deletion.SET_NULL, to='contract.contractmonthpay')),
            ],
            options={
                'verbose_name': 'Дневной платеж',
                'verbose_name_plural': 'Дневные платежи',
                'db_table': 'contract_day_pay',
            },
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
                ('percent', models.PositiveIntegerField(default=0)),
                ('date', models.DateField(null=True)),
                ('school', models.ForeignKey(db_column='school', null=True, on_delete=django.db.models.deletion.SET_NULL, to='school.school')),
            ],
            options={
                'verbose_name': 'Скидка',
                'verbose_name_plural': 'Скидки',
                'db_table': 'discount',
            },
        ),
        migrations.AddField(
            model_name='contract',
            name='discount',
            field=models.ManyToManyField(db_column='discount', related_name='discount', to='contract.discount'),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.CharField(max_length=255)),
                ('contract', models.ForeignKey(db_column='contract', null=True, on_delete=django.db.models.deletion.SET_NULL, to='contract.contract')),
            ],
            options={
                'verbose_name': 'Транзакция',
                'verbose_name_plural': 'Транзакции',
                'db_table': 'transaction',
            },
        ),
    ]

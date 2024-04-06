# Generated by Django 5.0.2 on 2024-04-06 22:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("authorization", "0004_alter_student_leave_alter_student_reason_leave"),
        ("contract", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contract",
            name="student",
            field=models.ForeignKey(
                db_column="student",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="contracts",
                to="authorization.student",
            ),
        ),
    ]

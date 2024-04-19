# Generated by Django 4.2.11 on 2024-04-19 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skills', '0004_alter_jobguide_job'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skill',
            name='value',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterUniqueTogether(
            name='skill',
            unique_together={('value', 'category')},
        ),
    ]
# Generated by Django 3.1.7 on 2021-06-05 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medical', '0018_auto_20210605_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicine',
            name='pending',
            field=models.IntegerField(),
        ),
    ]

# Generated by Django 2.1.7 on 2019-03-29 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mybooks', '0002_auto_20190329_2334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='isbn',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]

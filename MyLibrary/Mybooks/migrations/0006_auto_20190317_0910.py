# Generated by Django 2.1.7 on 2019-03-17 09:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Mybooks', '0005_auto_20190317_0819'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.FloatField(choices=[('1', 'No way'), ('2', 'Weak'), ('3', 'Nearly'), ('4', 'Interesting'), ('5', 'Good'), ('6', 'Very good'), ('7', "I can't tear myself away"), ('8', 'Masterpiece')])),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Mybooks.Book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Rate',
        ),
        migrations.AddField(
            model_name='book',
            name='rate',
            field=models.ManyToManyField(through='Mybooks.BookRate', to=settings.AUTH_USER_MODEL),
        ),
    ]
# Generated by Django 3.0.8 on 2021-02-17 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='description',
            field=models.TextField(max_length=4000, verbose_name='Описание'),
        ),
    ]
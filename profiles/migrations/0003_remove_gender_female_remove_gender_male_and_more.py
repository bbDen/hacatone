# Generated by Django 4.0.4 on 2022-04-30 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_category_gender_teacher_cat_alter_teacher_gender'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gender',
            name='female',
        ),
        migrations.RemoveField(
            model_name='gender',
            name='male',
        ),
        migrations.AddField(
            model_name='gender',
            name='gender',
            field=models.CharField(default=1, max_length=10, unique=True),
            preserve_default=False,
        ),
    ]

# Generated by Django 3.0.4 on 2022-03-31 11:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name': '用户数据', 'verbose_name_plural': '用户数据'},
        ),
    ]

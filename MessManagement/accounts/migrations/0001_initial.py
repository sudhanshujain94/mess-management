# Generated by Django 2.2.2 on 2019-07-09 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact_Us_Login',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roll_no', models.CharField(default='', max_length=10)),
                ('email', models.EmailField(default='', max_length=254)),
                ('description', models.TextField(default='')),
            ],
        ),
    ]
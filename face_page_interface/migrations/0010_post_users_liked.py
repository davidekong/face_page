# Generated by Django 4.1.2 on 2022-10-20 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('face_page_interface', '0009_post_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='users_liked',
            field=models.ManyToManyField(to='face_page_interface.customuser'),
        ),
    ]

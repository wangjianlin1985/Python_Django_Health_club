# Generated by Django 2.0.7 on 2020-04-08 21:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_course_teacher'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='teacher',
            new_name='usermessage',
        ),
    ]

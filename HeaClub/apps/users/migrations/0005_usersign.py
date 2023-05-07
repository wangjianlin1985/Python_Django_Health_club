import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_userfavorite'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('signdate', models.DateField(default=datetime.datetime(2020, 4, 11, 0, 20, 48, 313279))),
                ('day', models.CharField(max_length=3)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '用户签到表',
                'verbose_name_plural': '用户签到表',
            },
        ),
    ]

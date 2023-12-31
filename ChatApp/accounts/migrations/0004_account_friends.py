# Generated by Django 4.2.5 on 2023-10-17 09:10

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_account_interests_alter_userinterest_interest_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='friends',
            field=models.ManyToManyField(blank=True, related_name='user_friends', to=settings.AUTH_USER_MODEL),
        ),
    ]

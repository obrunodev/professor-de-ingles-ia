# Generated by Django 5.1.3 on 2024-11-08 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('englishbot', '0002_teacherprompt'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='about',
            field=models.TextField(blank=True, null=True, verbose_name='Sobre mim'),
        ),
        migrations.AddField(
            model_name='student',
            name='age',
            field=models.SmallIntegerField(default=18, verbose_name='Idade'),
        ),
        migrations.AddField(
            model_name='student',
            name='gender',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Gênero'),
        ),
    ]

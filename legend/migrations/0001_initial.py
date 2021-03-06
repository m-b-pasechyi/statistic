# Generated by Django 3.1.7 on 2021-05-29 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('string', models.CharField(help_text='Без служебных знаков', max_length=60, verbose_name='Строковое представление атрибута')),
                ('description', models.TextField(blank=True, verbose_name='Пояснения')),
            ],
            options={
                'verbose_name': 'Атрибут ответа',
                'verbose_name_plural': 'Атрибуты ответа',
            },
        ),
        migrations.CreateModel(
            name='Parameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.CharField(choices=[('Общие', 'Общие'), ('Фильтры', 'Фильтры')], max_length=10, verbose_name='Группа параметров')),
                ('string', models.CharField(help_text='Без служебных знаков', max_length=60, verbose_name='Строковое представление параметра')),
                ('descriprion', models.TextField(blank=True, verbose_name='Пояснения')),
            ],
            options={
                'verbose_name': 'Параметр запроса',
                'verbose_name_plural': 'Параметры запроса',
            },
        ),
    ]

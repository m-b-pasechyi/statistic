# Generated by Django 3.1.7 on 2021-07-28 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('own_parsers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='optionforparser',
            name='field_in_model',
            field=models.CharField(choices=[('Budget| Справочник бюджетов', (('id', 'id| ID'), ('guid', 'guid| Глобально-уникальный идентификатор записи'), ('code', 'code| Код'), ('name', 'name| Полное наименование'), ('parentcode', 'parentcode| Вышестоящий бюджет'), ('startdate', 'startdate| Дата начала действия записи'), ('enddate', 'enddate| Дата окончания действия записи'), ('status', 'status| Статус записи'), ('budgettype', 'budgettype| Тип бюджета'), ('okatocode', 'okatocode| Код ОКАТО'), ('oktmocode', 'oktmocode| Код ОКТМО'), ('tofkcode', 'tofkcode| Код ТОФК'), ('filedate', 'filedate| Дата создания записи(файла)'), ('loaddate', 'loaddate| Дата загрузки записи(файла)'))), ('GlavBudgetClass| Справочник главы по бюджетной классификации', (('id', 'id| ID'), ('guid', 'guid| Глобально-уникальный идентификатор записи'), ('code', 'code| Код'), ('name', 'name| Сокращенное наименование'), ('startdate', 'startdate| Дата начала действия записи'), ('enddate', 'enddate| Дата окончания действия записи'), ('budget', 'budget| Бюджет'), ('dateinclusion', 'dateinclusion| Дата включения кода'), ('dateexclusion', 'dateexclusion| Дата исключения кода'), ('year', 'year| Год')))], help_text='Не перепутайте поле модели', max_length=60, verbose_name='Поле модели для заполнения'),
        ),
    ]

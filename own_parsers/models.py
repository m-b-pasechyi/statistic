from django.db import models
from legend.models import Attribute
from maindb import models as mainmodels
#from django.apps import apps #для получения данных приложений в проекте

# Кусок не работает ввиду непрогрузки моделей на момент запроса apps
#MODELSDB = list(
#    zip(
#        tuple(i.__name__ for i in apps.get_app_config('maindb').get_models()),
#        tuple(i._meta.verbose_name for i in apps.get_app_config('maindb').get_models())
#        )
#        )
#
#FIELDSOFMODEL = list(
#    (
#        f'{i[0]}| {i[1]}',
#        tuple(
#            (a.name, a.verbose_name) for a in apps.get_model('maindb',i[0])._meta.fields
#            )
#    )
#    for i in MODELSDB
#    )
#

MODELSDB = list( tuple((i.__name__,i._meta.verbose_name) for i in(
            filter(lambda i: i.__class__.__name__=='ModelBase',
                (getattr(mainmodels,i) for i in mainmodels.__dict__.keys())
                )
        ))
        )

FIELDSOFMODEL = list(
    (
        f'{i[0]}| {i[1]}',
        tuple(
            (a.name, f'{a.name}| {a.verbose_name}') for a in getattr(mainmodels,i[0])._meta.fields
            )
    )
    for i in MODELSDB
    )

class OptionForParser(models.Model):

    field_in_json = models.ForeignKey(
        verbose_name = "Поле в JSON",
        to=Attribute,
        on_delete = models.DO_NOTHING,
    )

    model_of_db = models.CharField(
        verbose_name = "Модель для заполнения",
        help_text = "Выбор результирующей модели",
        max_length = 60,
        choices = MODELSDB,
    )

    field_in_model = models.CharField(
        verbose_name = "Поле модели для заполнения",
        help_text = "Не перепутайте поле модели",
        max_length = 60,
        choices = FIELDSOFMODEL,    
    )

    description = models.CharField(
        verbose_name = "Описание",
        max_length = 140,
        blank =  True,
    )

    class Meta:
        verbose_name = "Параметр сериализвтора"
        verbose_name_plural = "Параметры сериализвтора"
    
    def short_description(self):
        return f'{self.field_in_json}->{self.field_in_model}'
    
    def __str__(self):
        return f'{self.field_in_json}-->{self.model_of_db}| {self.field_in_model}'

class ParserConfig(models.Model):

    options = models.ManyToManyField(
        verbose_name = "Параметры для сериализатора",
        to = OptionForParser,
        blank = False,
        
    )

    description = models.TextField(
        verbose_name = "Пояснение",
        blank = True,
    )

    def __str__(self):
        if not self.description:
            return '; '.join(list(i.short_description().replace('\r\n',' ') for i in list(self.options.all())))
        else:
            return self.description[:140]
    class Meta:
        verbose_name = "Конфигурация сериализатора для заполнения БД"
        verbose_name_plural = "Конфигурации сериализатора для заполнения БД"

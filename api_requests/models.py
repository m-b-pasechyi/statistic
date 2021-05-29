from django.db import models
from legend.models import Parameter
import string
# Create your models here.
class OptionForAPI(models.Model):

    parameter = models.ForeignKey(
        Parameter,
        on_delete=models.DO_NOTHING,
        verbose_name="Параметр запроса",
        )

    value = models.CharField(
        verbose_name="Значение параметра",
        help_text="Цифры,знаки",
        max_length=20,
        blank=False,
    )

    def generate_string(self):
        return f'{self.parameter.string}={self.value}'

    class Meta:
        verbose_name = "Пара параметр-значение"
        verbose_name_plural = "Пары параметр-значение"

    def __str__(self):
        return f'{self.parameter.group}| {self.parameter} = {self.value}'


class RequestForApi(models.Model):

    addres = models.CharField(
        verbose_name="Адрес для API запросов",
        blank=False,
        max_length=150,
    )
    
    parameters = models.ManyToManyField(
        to = OptionForAPI,
        verbose_name="Параметры",
        blank=True,
    )
    
    
    description = models.TextField(
        verbose_name="Пояснение",
        blank=True,
    )

    def generate_string(self):
        par_list = list(i.generate_string() for i in tuple(self.parameters.all()))
        par_string = '&'.join(par_list) 
        return ''.join(filter(lambda x: x in string.printable and x!=' ', f'{self.addres}?{par_string}'))
    
    def __str__(self):
        return f'id {self.id}| {self.description[:60]}'


    class Meta:
        verbose_name = "Запрос для внешней БД"
        verbose_name_plural = "Запросы для внешней БД"
from django.db import models
from legend.models import Parameter, Attribute
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
    
    def __init__(self,*args,**kwargs): 
        super().__init__(*args,**kwargs)
        #подчистка строки адреса от пробелов при инициализации
        self.addres=''.join(filter(lambda x: x in string.printable and x!=' ', self.addres))
        
    
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

    """def save(self,*args,**kwargs):
        addres = ''.join(filter(lambda x: x in string.printable and x!=' ',self.addres))
        super().save(*args,**kwargs)"""

    def generate_string(self):
        par_list = list(i.generate_string() for i in tuple(self.parameters.all()))
        par_string = '&'.join(par_list) 
        return ''.join(filter(lambda x: x in string.printable and x!=' ', f'{self.addres}?{par_string}'))
    
    def __str__(self):
        return f'id {self.id}| {self.description[:60]}'


    class Meta:
        verbose_name = "Запрос для внешней БД"
        verbose_name_plural = "Запросы для внешней БД"

class CompilationR(models.Model):

    initial_request = models.ForeignKey(
        'RequestForApi',
        verbose_name="Главный запрос",
        on_delete=models.DO_NOTHING
        )
        
    get_page = models.ForeignKey(
        Parameter,
        verbose_name="Запрос страницы",
        on_delete=models.DO_NOTHING,
        related_name='get_page',
        blank=True,
        default='',
        null=True,
        )
        
    get_code = models.ForeignKey(
        Parameter,
        verbose_name="Запрос кода",
        on_delete=models.DO_NOTHING,
        related_name='get_code',
        blank=True,
        default='',
        null=True,
        )

    get_data = models.ForeignKey(
        Attribute,
        verbose_name="Данные со страницы",
        on_delete=models.DO_NOTHING,
        related_name='get_data',
        blank=True,
        default=None,
        null=True,
        )

    get_page_count = models.ForeignKey(
        Attribute,
        verbose_name="Общее количество страниц в теле ответа",
        on_delete=models.DO_NOTHING,
        related_name='get_page_count',
        blank=True,
        default='',
        null=True,
        )
    
    get_record_count = models.ForeignKey(
        Attribute,
        verbose_name="Общее количество записей в теле ответа",
        on_delete=models.DO_NOTHING,
        related_name='get_record_count',
        blank=True,
        default='',
        null=True,
        )

    get_current_page_number = models.ForeignKey(
        Attribute,
        verbose_name="Текущий номер страницы в теле ответа",
        on_delete=models.DO_NOTHING,
        related_name='get_current_page_number',
        blank=True,
        null=True,
        )

    

        
        
    class Meta:
        verbose_name = "Сборник запросов для скачивания БД"
        verbose_name_plural = "Сборники запросов для скачивания БД"
        
    def __str__(self):
        return f'id {self.id}| {self.initial_request.description[:60]}'




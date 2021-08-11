from django.db import models
import datetime
from django.contrib import admin
# Create your models here.
class KBKStatus(models.TextChoices):
    ACTIVE = "ACTIVE", 'Актуальная запись'
    ARCHIVE = "ARCHIVE", 'Архивная запись'


class BudgetType(models.TextChoices):
    """Код типа бюджета"""
    OTHER = "00", 'Прочие бюджеты'
    FEDERAL = "01", 'Федеральный бюджет'
    SUBJECT = "02", 'Бюджет субъекта РФ'
    CAPITALS = "03", 'Бюджеты внутригородских МО г. Москвы и г. Санкт-Петербурга'
    CITY = "04", 'Бюджет городского округа'
    MUNICIPAL = "05", 'Бюджет муниципального района'
    PENSION = "06", 'Бюджет Пенсионного фонда РФ'
    FSS = "07", 'Бюджет ФСС РФ'
    FFOMS = "08", 'Бюджет ФФОМС'
    TFOMS = "09", 'Бюджет ТФОМС'
    LOCAL = "10", 'Бюджет поселения'
    #Есть 13 код в документации не описан, возможно есть и другие
    DISTRIBUTED = "98", 'Распределяемый доход'
    ORGANIZATION = "99", 'Доход организации (только для ПДИ)'
    __empty__ = '(Unknown)'


class Budget(models.Model):
   
    guid= models.CharField(
        "Глобально-уникальный идентификатор записи",
        max_length=36,
        unique=True,
        )  # ! Не берем при импорте
   
    code= models.CharField(
        "Код",
        max_length=8,
        blank=False,
        default=None,
        )

    name= models.TextField(
        "Полное наименование",
        max_length=2000,
        blank=False,
        null=False
        )

    parentcode = models.ForeignKey(
        'self',
        verbose_name="Вышестоящий бюджет",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        )
 
    startdate = models.DateTimeField(
        "Дата начала действия записи",
        blank=True,
        null=True,
        default=None,
        )

    enddate = models.DateTimeField(
        "Дата окончания действия записи",
        blank=True,
        null=True,
        default=None
        )

    status = models.CharField(
        "Статус записи",
        max_length=7,
        choices=KBKStatus.choices,
        blank=False,
        null=False,
        default=KBKStatus.ACTIVE
        )

    budgettype = models.CharField(
        "Тип бюджета",
        max_length=2,
        choices=BudgetType.choices,
        blank=False,
        null=False,
        default=BudgetType.OTHER
        )

    okatocode=models.CharField(
        verbose_name="Код ОКАТО",
        help_text='Общероссийский классификатор объектов административно-территориального деления https://classifikators.ru/okato',
        max_length=11,
        blank=True,
        )

    oktmocode=models.CharField(
        verbose_name="Код ОКТМО",
        help_text='Общероссийский классификатор территорий муниципальных образований (сокращ. ОКТМО) — классификатор объектов административно-территориального деления Российской Федерации, входит в состав «Единой системы классификации и кодирования технико-экономической и социальной информации Российской Федерации» (ЕСКК). https://oktmorus.ru',
        max_length=11,
        blank=True,
        )

    tofkcode=models.CharField(
        verbose_name="Код ТОФК",
        help_text='Территориальный орган Федерального казначейства',
        max_length=4,
        blank=True,
        )

    filedate=models.DateTimeField(
        verbose_name="Дата создания записи(файла)",
        blank=True,
        default=None,
        )
    
    loaddate=models.DateTimeField(
        verbose_name="Дата загрузки записи(файла)",
        blank=True,
        default=None,
        )

   
    class Meta:
        verbose_name = 'Справочник бюджетов'
        verbose_name_plural = 'Справочники бюджетов'
        unique_together = ('code','startdate')
    
    @property
    def level(self):    
        """Возврат уровня записи в общей иерархии от 1 до бесконечности, чем больше, тем ниже"""
        def get_code_level(code=self.code, level=1):
            ret = self.__class__.objects.get(code=code)
            if ret.parentcode == None:
                return level
            else:
                level+=1
                return get_code_level(ret.parentcode.code,level=level)
        return get_code_level()
    level.fget.short_description = "Иерархия записи"#для  отображения названия столбца в админке
    
    @property
    def fs_offsprings(self):

        """Потомки следующей ступени"""
        if self.__class__.objects.filter(parentcode=self.pk).exists():
            return self.__class__.objects.filter(parentcode=self.pk)

    


    def __str__(self):
        return f"{self.code}: {self.name}"


class GlavBudgetClass(models.Model):
    """Справочник главы по бюджетной классификации."""
    
    guid = models.CharField(
        "Глобально-уникальный идентификатор записи",
        max_length=36
        )

    code = models.CharField(
        "Код",
        max_length=3,
        blank=False,
        null=False
        )  # ! если не будут пересекаться добавить: , unique=True
   
    name = models.TextField(
        "Сокращенное наименование",
        max_length=254,
        blank=True,
        null=True
        )

    startdate = models.DateTimeField(
        "Дата начала действия записи",
        blank=False,
        null=False,
        default=datetime.datetime.now
        )

    enddate = models.DateTimeField(
        "Дата окончания действия записи",
        null=True
        )

    budget = models.ForeignKey(
        Budget,
        verbose_name="Бюджет",
        blank=False,
        null=False,
        on_delete=models.CASCADE
        )

    dateinclusion = models.DateTimeField(
        "Дата включения кода",
        blank=False,
        null=False,
        default=datetime.datetime.now
        )

    dateexclusion = models.DateTimeField(
        "Дата исключения кода"
        )

    year = models.DateField(
        "Год"
        )
   
    class Meta:
        verbose_name = 'Справочник главы по бюджетной классификации'
        verbose_name_plural = 'Справочники главы по бюджетной классификации'


    def __str__(self):
        return f"{self.code}: {self.name}"


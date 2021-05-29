from django.db import models

class Parameter(models.Model):
    GROUPS = (
        ('Общие','Общие'),
        ('Фильтры','Фильтры'),
    )
    group = models.CharField(
        verbose_name="Группа параметров",
        choices=GROUPS,
        max_length=10,
    )
    string = models.CharField(
        verbose_name="Строковое представление параметра",
        help_text="Без служебных знаков",
        max_length=60,
    )

    descriprion = models.TextField(
        verbose_name="Пояснения",
        blank=True,
    )

    class Meta:
        verbose_name = "Параметр запроса"
        verbose_name_plural = "Параметры запроса"
    
    def __str__(self):
        return self.string +' | '+self.descriprion[:self.descriprion.find('.')]


class Attribute(models.Model):

    string = models.CharField(
        verbose_name="Строковое представление атрибута",
        help_text="Без служебных знаков",
        max_length=60,
        )

    description = models.TextField(
        verbose_name="Пояснения",
        blank=True,
        )

    class Meta:
        verbose_name = "Атрибут ответа"
        verbose_name_plural = "Атрибуты ответа"
    
    def __str__(self):
        return self.string +' | '+self.description[:self.description.find('.')]
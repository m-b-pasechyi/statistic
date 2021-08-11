from django.contrib import admin
from .models import Budget
from django.db import models
from django.forms import SelectMultiple


#удобочитаемый фильтр по родительским элементам в админке
class OffspringFilter(admin.SimpleListFilter):
    """Медленный до жути аналог RelatedOnlyFieldFilter """
    title='Фильтр по родительскому коду'
    parameter_name='parentcode'

    def lookups(self,request,model_admin):
        qs=model_admin.get_queryset(request)
        if qs.exists():
            for i in qs:
                if qs.filter(parentcode=i).exists():
                    yield (i.pk,f'{i.code} {i.name}')
    def queryset(self,request,queryset):
        print('value:',self.value())
        return queryset.filter(parentcode__pk=self.value())




class MaindbAdmin(admin.ModelAdmin):
    list_display = ('code','name','level','parentcode',)
    list_filter=(('parentcode',admin.RelatedOnlyFieldListFilter),)

admin.site.register(Budget,MaindbAdmin)





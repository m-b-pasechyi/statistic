from django import template

register = template.Library()

@register.filter
def verbose_name(object,field_name):
    """Фильтр шаблона для вывода вербального имени поля. Применим к объекту, принимает имя поля"""
    try:
        #список полей из _meta фильруем на предмет совпадения с именем поля
        r=tuple(i for i in filter(lambda x: x.name==field_name, object._meta.fields))[0].verbose_name
    except:
        #если в списке полей нет данного имени, то берём вербальное имя из атрибута (фича добавлена в модели)
        r=getattr(object,field_name).verbose_name
    return r
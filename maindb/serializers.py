from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Budget, BudgetType
import datetime
import requests
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist,MultipleObjectsReturned


class InDbValidator:
    serializer_context = True

    def __call__(self,value,serializer_field):
        if not serializer_field.objects.get(code = value).exists():
            raise serializers.ValidationError(detail='Have no parentcode object in DB.',code=1007)

def clear_of(data,subj='',target=None,key1=False,process_func=False):
    """
    Реверсивный алгоритм.
    Очистка исходных данных от целевого значения c заменой,
    с возможностью выбора ключа и обработки исходного значения:
    data - исходные данные;
    subj-строка для поиска, ну или любой другой тип;
    target-данные для замены найденного;
    key1- ключ для поиска;
    process_func- функция обрабатывающаяя исходное значение
    """
    def process(value,process_func=process_func):
        """
         
        """
        if process_func:
            try:
                return process_func(value)
            except:
                pass
        else:
            return value

    if type(data)==dict:
        for key, value in data.items():
            if type(value) not in (set,tuple,dict,list):
                if key1:
                    conditions = (process(value)==subj, key==key1)
                else:
                    conditions = (process(value)==subj,)
                try:
                    if all(conditions):
                        data[key]=target
                except:
                    break
            else:
                clear_of(value, subj=subj,target=target,key1=key1,process_func=process_func)
    elif type(data) in (set,tuple,list):
        for i in data:
            clear_of(i, subj=subj,target=target,key1=key1,process_func=process_func)
    return data


class BudgetSerializer(serializers.ModelSerializer):
    
    enddate=serializers.DateTimeField(required=False,allow_null=True)
    
    def to_internal_value(self,data):
        parentcode = data.get('parentcode',None)
        
        if parentcode == '':
            parentcode = None
        elif parentcode == None:
            parentcode = parentcode
        elif isinstance(parentcode,self.Meta.model):
            parentcode = data['parentcode']
        elif int(parentcode) == 0:
            parentcode = None
        elif parentcode == data['code']:
            parentcode = None
        else:
            try:
                parentcode = self.Meta.model.objects.get(code=str(parentcode)).pk
            except MultipleObjectsReturned:
                parentcode = self.Meta.model.objects.filter(code=str(parentcode),status='ACTIVE').first().pk
            except Exception as exc:
                print('STATUS',data['status'])
        
        enddate = data.get('enddate',None)
        if enddate == '':
            enddate = None

        data.update({'parentcode':parentcode,'enddate':enddate})
        print ('data_to_internal:',data)
        return super().to_internal_value(data)

    def validate_guid(self,value):
        if not self.instance:
            if self.Meta.model.objects.filter(guid=value).exists():
                raise ValidationError("Уже существует запись",code="guid_unique")
        else:
            pass
        return value
    
        
    class Meta:
        model = Budget
        fields =  '__all__'
        

    
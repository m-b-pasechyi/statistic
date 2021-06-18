from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Budget, BudgetType
import datetime




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
                    print(process(value),':', process(value).__class__)
                else:
                    conditions = (process(value)==subj,)
                    print(process(value),':', process(value).__class__)
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


class BudgetSerializer(serializers.ModelSerializer):
    
    enddate=serializers.DateTimeField(required=False,allow_null=True)
    
    def is_valid(self, raise_exception=False):
        """ Перед основной валидацией добавлена очистка инициализирующих данных """
        clear_of(self.initial_data)
        clear_of(self.initial_data,key1='parentcode',process_func=int,subj=0)
        return super().is_valid(raise_exception)

    
    
    def to_representation(self,instance):
        newinstance = super().to_representation(instance)
        if newinstance['enddate']=='':
            newinstance['enddate']=None
        return newinstance
    
    
    def to_internal_value(self,data):
        newdata = super().to_internal_value(data)
        if newdata['enddate']=='':
            newdata['enddate']=None
        return newdata

    #enddate= serializers.DateField(format="%Y-%m-%d",allow_null=True,required=False)

    class Meta:
        model = Budget
        fields = '__all__'

    
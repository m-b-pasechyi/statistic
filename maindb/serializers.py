from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Budget, BudgetType
import datetime




def clear_of(data,subj='',target=None):
    if type(data)==dict:
        for key, value in data.items():
            if type(value) not in (set,tuple,dict,list):
                if value == subj:
                    data[key]=target
            else:
                let_see(value)
    elif type(data) in (set,tuple,list):
        for i in data:
            let_see(i)


class BudgetSerializer(serializers.ModelSerializer):
    
    enddate=serializers.DateField(required=False,allow_null=True)
    
    def is_valid(self, raise_exception=False):
        clear_of(self.initial_data)
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

    
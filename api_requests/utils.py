import requests
from api_requests.models import RequestForApi
from maindb.serializers import BudgetSerializer


def generate_json_resp():
    return requests.get(RequestForApi.objects.first().generate_string()).json()


def clear_of(data,subj='',target=None):
    if type(data)==dict:
        for key, value in data.items():
            if type(value) not in (set,tuple,dict,list):
                if value == subj:
                    data[key]=target
                print (key,":--",value)
            else:
                let_see(value)
    elif type(data) in (set,tuple,list):
        for i in data:
            let_see(i)


def try_again(l):
    resp1 = requests.get(RequestForApi.objects.first().generate_string())
    data1 = resp1.json()['data'][l]
    """for k,v in data1.items():
        if v=='':
            data1[k]=None"""
    
    return BudgetSerializer(data1,data=data1)
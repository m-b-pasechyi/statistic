import requests
from api_requests.models import RequestForApi
from maindb.serializers import BudgetSerializer


def generate_json_resp():
    return requests.get(RequestForApi.objects.first().generate_string()).json()





def try_again(l):
    resp1 = requests.get(RequestForApi.objects.get(id=2).generate_string())
    data1 = resp1.json()['data'][0]
    """for k,v in data1.items():
        if v=='':
            data1[k]=None"""
    
    return BudgetSerializer(data1,data=data1)
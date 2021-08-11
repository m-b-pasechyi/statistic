import requests
from api_requests.models import RequestForApi
from maindb.serializers import BudgetSerializer
from maindb.models import Budget
import datetime
from django.db.models import Q
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from api_requests.models import CompilationR
import copy

timeouted_records = []
other_records=[]

def generate_json_resp():
    return requests.get(RequestForApi.objects.first().generate_string()).json()

def try_again(i,p,compilation_item = CompilationR.objects.last()):
    initial_addres = compilation_item.initial_request.addres
    print(initial_addres)
    parameters = {i.parameter.string:i.value for i in compilation_item.initial_request.parameters.all()}
    print(parameters)
    parameters.update({compilation_item.get_page.string:p})
    first_page_response = requests.get(initial_addres,parameters)
    data1 = first_page_response.json()['data'][i]
    """for k,v in data1.items():
        if v=='':
            data1[k]=None"""
    
    return BudgetSerializer(data1,data=data1)

def particular_request(code,compilation_item=CompilationR.objects.last(),startdate=datetime.datetime.now(),enddate=datetime.datetime.now(),status='ACTIVE',**kwargs):
    """
    Получить: сводный запрос, код родительского элемента, дату начала и конца действия дочернего элемента
    вернуть: единственную удовлетворительную запись (словарь)
    """

    def str_to_datetime(dt_string,dt_format='%Y-%m-%d %H:%M:%S.%f'):
        """Из строкового значения в datetime формат """
        if dt_string==None or dt_string=='':
            dt_string = datetime.datetime.now()
        if type(dt_string)==str:
            dt_string = datetime.datetime.strptime(dt_string,dt_format)
        return dt_string

    startdate = str_to_datetime(startdate)
    enddate = str_to_datetime(enddate)

    initial_addres = compilation_item.initial_request.addres
    parameters = {i.parameter.string:i.value for i in compilation_item.initial_request.parameters.all()}
    get_code = compilation_item.get_code.string
    get_status = 'filterstatus'
    current_code_dict =  {get_code:str(code)}
    if status!=None:
        current_status_dict = {get_status:status}
        parameters.update(current_status_dict)
    else:
        try:
            parameters.pop('filterstatus')
        except:
            pass
    
    parameters.update(current_code_dict)
    if kwargs:
        parameters.update(kwargs)
    print (parameters)
    try:
        current_response = requests.get(initial_addres,parameters,timeout=(5,5))
    except:
        return timeouted_records.append(code)
    data = compilation_item.get_data.string
    ret = [
        i for i in current_response.json()[data] 
        if startdate >= str_to_datetime(i['startdate']) 
        and enddate<=str_to_datetime(i['enddate'])
        ]
    
    if len(ret)==1:
        ret = ret[0]
        
    elif len(ret)==0:
        try:
            ret = [i for i in current_response.json()[data]][0]
        except:
            ret = None
    else:
        ret = ret[-1]

    return ret


def find_hidden_parentcode(record,compilation_item = CompilationR.objects.last()):
    """Поиск кода (code)  родительского элемента с активным статусом(status:'ACTIVE').
    Все архивные родительские записи игнорируюстя, и возвращается первая активная.
    """
    parent_record = particular_request(
        code = str(record['parentcode']),
        startdate=record['startdate'],
        enddate=record['enddate'],
        status='ACTIVE',
        compilation_item=compilation_item)
    
    if parent_record!=None:# если родительская запись активна, возвращаем её код
        if parent_record['status'] == 'ACTIVE':
            return parent_record['code']

    else:#Иначе находим архивную и используем её в качестве аргумента для нашей функции при рекурсии.
        parent_record = particular_request(
        code = str(record['parentcode']),
        startdate=record['startdate'],
        enddate=record['enddate'],
        status='ARCHIVE',
        compilation_item=compilation_item)
        
        return find_hidden_parentcode(parent_record,compilation_item = compilation_item)#Рекурсия остановится при нахождении "Активной" записи. 
    
    




def start_request(compilation_item = CompilationR.objects.last()):
    """Производство первоначального запроса по адресу из обобщающего класса (поумолчанию - последний из созданных).
    """
    initial_addres = compilation_item.initial_request.addres
    parameters = {i.parameter.string:i.value for i in compilation_item.initial_request.parameters.all()}
    first_page_response = requests.get(initial_addres,parameters)
    page_count = first_page_response.json()[compilation_item.get_page_count.string]
    record_count = first_page_response.json()[compilation_item.get_record_count.string]
    get_page = compilation_item.get_page.string
    data = compilation_item.get_data.string


    def serialize_and_create(record):
        """Сериализация словаря из списка данных (['data']), пришедшего по запросу json. С последующим вызовом валидации
        и созданием записи в БД.  
        """
        current_serializer = BudgetSerializer(record,data=record)
        current_serializer.instance = None

        if current_serializer.is_valid():
            current_serializer.create(current_serializer.validated_data)
            print('success :',current_serializer.validated_data['name'],current_serializer.validated_data['code'])
        else:
            print ('plan_b :')
            print(current_serializer.errors)

            if 'parentcode' in current_serializer.errors.keys():
                code = find_hidden_parentcode(record,compilation_item = compilation_item)
                parent_record = particular_request(
                    compilation_item = compilation_item,
                    code = code,
                    startdate=record['startdate'],
                    enddate=record['enddate'],
                    status='ACTIVE')#None заменил на 'ACTIVE'
                record['parentcode']=code

                serialize_and_create(parent_record)
                return serialize_and_create(record)
                
            
            elif 'guid' in current_serializer.errors.keys():
                return           
            else:
                other_records.append(record)


    for i in range(page_count):#постраничный перебор посредством добавления в параметры запроса помера новой страницы.
        #filterpage=i
        parameters.update({get_page:i})
        try:
            current_response = requests.get(initial_addres,parameters,timeout=(5,5))
            current_page_data = current_response.json()[data]
        except:
            print ('похоже, страницу не получить')
        a=-1
        for record in current_page_data:#перебор записей в списке 'data'
            a+=1
            serialize_and_create(record)
    return timeouted_records

def check_and_update(compilation_item = CompilationR.objects.last()):
    """Проверка всех записей в бд относящихся к текущей модели на свежесть и их обновление при более свежей записи загрузки
    """
    item_with_maximal_loaddate = Budget.objects.latest('loaddate')
    print ('item_with_maximal_loaddate',item_with_maximal_loaddate.__dict__)
    
    #этот участок кода (10 строк) надо переписать, он во многом повторяет функцию start_request
    initial_addres = compilation_item.initial_request.addres
    parameters = {i.parameter.string:i.value for i in compilation_item.initial_request.parameters.all()}
    get_page = compilation_item.get_page.string
    data = compilation_item.get_data.string
    #filteloaddate работает как нестрогое неравенство, учитывет дни. Добавим разницу в один день к максимально найденной
    #дате загрузки
    parameters.update({'filterminloaddate':(item_with_maximal_loaddate.loaddate+datetime.timedelta(days=1)).strftime('%d.%m.%Y')})
    first_page_response = requests.get(initial_addres,parameters)
    print('first_page_response.json()',first_page_response.json())
    page_count = first_page_response.json()[compilation_item.get_page_count.string]
    record_count = first_page_response.json()[compilation_item.get_record_count.string]
    print('record_count',record_count)
    if record_count in (0,None,''):
    #смело допустим, что справочник не будут менять задним числом 
        return 'Изменений не произошло, обновлять нечего'
    else:
        #начинаем постраничный перебор с последующим рассмотрением элементов списка
        print ('page_count',page_count)
        for i in range(page_count):
            #постраничный перебор посредством добавления в параметры запроса помера новой страницы.
            #filterpage=i
            parameters.update({get_page:i})
            print ('parameters',parameters)
            try:
                current_response = requests.get(initial_addres,parameters,timeout=(5,5))
                current_page_data = current_response.json()[data]
            except:
                print ('похоже, страницу не получить')
            for record in current_page_data:#перебор записей в списке 'data'
                instance = Budget.objects.filter(code=record['code'],status=record['status']).last()
                print ('instance',type(instance))
                record.update({'pk':instance.id})
                print ('record',record)

                
                
                s=BudgetSerializer(instance=instance,data=record)
                if s.is_valid():
                    s.update(instance=instance, validated_data=s.validated_data)
                    print ('updated')
        return
            








#--------------------------------------- наброски, к основному коду не причастны
def get_all_codes(compilation_item = CompilationR.objects.last()):
    initial_addres = compilation_item.initial_request.addres
    parameters = {i.parameter.string:i.value for i in compilation_item.initial_request.parameters.all()}
    first_page_response = requests.get(initial_addres,parameters)
    page_count = first_page_response.json()[compilation_item.get_page_count.string]
    record_count = first_page_response.json()[compilation_item.get_record_count.string]
    get_page = compilation_item.get_page.string
    data = compilation_item.get_data.string

    all_codes = []
    for i in range(page_count):
        parameters.update({get_page:i})
        try:
            current_response = requests.get(initial_addres,parameters,timeout=(5,5))
            current_page_data = current_response.json()[data]
        except:
            print ('похоже, страницу не получить')
        a=-1
        for record in current_page_data:
            all_codes.append(record['code'])
            print ('CODE:',record['code'])

    return all_codes


def get_code_level(cd,level=1):
    ret = Budget.objects.get(code=cd)
    if ret.parentcode == None:
        return level
    else:
        level+=1
        return get_code_level(ret.parentcode.code,level=level)


def get_tree(code):
    ret={Budget.objects.get(code=code):[get_tree(i) for i in Budget.objects.filter(parentcode__code = code)]}
    
    
    return ret







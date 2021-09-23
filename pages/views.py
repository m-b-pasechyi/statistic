from django.views.generic.base import TemplateView
from django.views.generic import ListView
from maindb.models import Budget
from django.http import JsonResponse
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from django.core import serializers
# Create your views here.

class JSONResponseMixin:
    def render_to_json_response(self,context,**response_kwargs):
        return JsonResponse(
            self.get_data(context),safe=False,
            **response_kwargs,
        )
    
    def get_data(self, context):
        """
        Returns an object that will be serialized as JSON by json.dumps().
        """
        print (context)
        page_obj = context['page_obj']
        paginator = context['paginator']
        
        page = {
            'first':1 if page_obj.has_previous() else None,
            'previous':page_obj.previous_page_number() if page_obj.has_previous() and page_obj.previous_page_number()!=1 else None,
            'current':page_obj.number if paginator.num_pages!=1 else None,
            'next':page_obj.next_page_number() if page_obj.has_next() else None,
            'last':paginator.num_pages if page_obj.has_next() and paginator.num_pages!=page_obj.next_page_number() else None,
            }

        data ={'page':page,
        'object_list':[{
            'pk':i.pk,
            'name':i.name,
            'fs_offsprings':{'count':i.fs_offsprings_count,'url':i.fs_offsprings_url},
            } for i in context['object_list']],}
        print (data)
        
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        return data









class Index(JSONResponseMixin,ListView):
    
    model =  Budget
    allow_empty=False
    context_object_name = 'budget_list'
    paginate_by=20
    template_name='pages/index.html'
    ordering=['id']

    def get_queryset(self):
        pk=self.kwargs.get('pk',None)
        #if self.request.is_ajax():
        orderings=self.request.GET.get('orderings',None)
        filters=self.request.GET.get('filters',None)
        print(filters,' # ',orderings)
        print('!!!!SESSION: ',self.request.session.set_test_cookie(),self.request.session.test_cookie_worked())    
        print(self.request.is_ajax())
        return super().get_queryset().filter(parentcode=pk)
    
    def render_to_response(self, context, **response_kwargs):
        """Переопределяем для возврата JSON при запросе от ajax"""
        if self.request.is_ajax():#проверка на ajax
            return self.render_to_json_response(context, **response_kwargs)#смотри на JSONresponseMixin
        else:
            return super().render_to_response(context, **response_kwargs)#своим чередом
    
    
    
    #def render_to_response(self,context,*args, **response_kwargs):
        #print (context)
        #return super().render_to_response(context, **response_kwargs)    

class Main_list_json(Index):
    template_name=None
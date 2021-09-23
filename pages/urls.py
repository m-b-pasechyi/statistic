from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('',views.Index.as_view(),name='index'),
    path('<int:pk>',views.Index.as_view(),name='fs_offsprings'),
    path('json/<int:pk>',views.Main_list_json.as_view(),name='json_list'),
    ]
from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('',views.Index.as_view(),name='index'),
    ]
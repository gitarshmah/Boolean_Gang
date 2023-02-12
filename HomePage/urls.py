
from django.urls import path, include
from . import views

app_name = 'HomePage'

urlpatterns = [
    path('HomePage/', include('HomePage.urls')),
    path('', views.index, name='index'),
]

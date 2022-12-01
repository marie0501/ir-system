from django import views
from django.urls import path
from . import views

urlpatterns=[
    path('', views.index, name = 'index'),
    path('results/<slug:documents_file>/', views.results, name='results')
]
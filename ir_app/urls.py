from django import views
from django.urls import path
from . import views



urlpatterns=[
    path('', views.index, name = 'index'),
    path('results/', views.results, name='results'),
    path('document/<int:id>/', views.document, name='document')
]
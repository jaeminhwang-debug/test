from django.urls import path
from . import views

urlpatterns = [
    path('structure/', views.structure_list, name='structure_list'),
    path('structure/<int:bs_id>/field/', views.field_list, name='field_list'),
    path('field/', views.field_list, name='field_list'),
    path('plot/', views.plot, name='plot'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('define/', views.define_structure, name='define_structure'),
    path('plot/', views.plot, name='plot'),
]

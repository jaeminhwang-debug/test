from django.urls import path, re_path
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('binstruct/', views.binstruct_list, name='binstruct_list'),
    path('binstruct/field/', views.binfield_list, name='binfield_list'),
    path('binstruct/<int:bs_id>/', views.binfield_list, name='binfield_list'),
    path('bindata/', views.bindata_list, name='bindata_list'),
    re_path(r'^{root}(?P<y>[0-9]{{4}})/(?P<m>[0-9]{{2}})/(?P<d>[0-9]{{2}})/(?P<n>.+)'.format(root=settings.UPLOAD_ROOT),
        views.bindata_download, name='bindata_download'),
    path('plot/', views.plot, name='plot'),
]

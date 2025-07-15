from django.urls import path, re_path
from django.urls import include
from . import views

urlpatterns = [
    path('', views.index_view),
    path('query/', views.query_view),
    re_path('query_main', views.query_main_back_info),
    re_path('del', views.query_delete_back_info),
    re_path('upload',views.upload_view),
]